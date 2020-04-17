from django.db import models


class MemberMeetingRelation(models.Model):
    meeting = models.ForeignKey('meetings.Meeting', on_delete=models.CASCADE)
    member = models.ForeignKey('users.User', on_delete=models.CASCADE)
    MEMBER_MANAGER, MEMBER_STUDENT = 'manager', 'student'
    MEMBER_TYPE_CHOICES = (
        (MEMBER_MANAGER, '관리자'),
        (MEMBER_STUDENT, '학생'),
    )
    member_type = models.CharField(max_length=5, choices=MEMBER_TYPE_CHOICES, null=False)

    class Meta:
        unique_together = [['meeting', 'member'],]


class Meeting(models.Model):

    title = models.CharField(max_length=30)
    host = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='+')
    members = models.ManyToManyField('users.User', related_name='meetings', through='meetings.MemberMeetingRelation')

    def __str__(self):
        return self.title
