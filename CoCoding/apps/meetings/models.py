from django.db import models


class MeetingMemberRelation(models.Model):
    meeting = models.ForeignKey('meetings.Meeting', on_delete=models.CASCADE)
    member = models.ForeignKey('users.User', on_delete=models.CASCADE)
    MEMBER_MANAGER, MEMBER_STUDENT = 'manager', 'student'
    MEMBER_TYPE_CHOICES = (
        (MEMBER_MANAGER, '관리자'),
        (MEMBER_STUDENT, '학생'),
    )
    member_type = models.CharField(max_length=10, choices=MEMBER_TYPE_CHOICES, null=False)

    class Meta:
        unique_together = [['meeting', 'member'], ]


class Meeting(models.Model):
    title = models.CharField(max_length=30, default='Untitled')
    host = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='+')
    members = models.ManyToManyField('users.User', related_name='meetings', through='meetings.MeetingMemberRelation')

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Meeting, self).save(force_insert, force_update, using, update_fields)
        MeetingMemberRelation.objects.get_or_create(
            member=self.host,
            meeting=self,
            member_type=MeetingMemberRelation.MEMBER_MANAGER
        )
