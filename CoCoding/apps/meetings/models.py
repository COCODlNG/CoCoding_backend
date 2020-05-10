from django.db import models
from django.urls import reverse_lazy
from django_extensions.db.models import TimeStampedModel


class MeetingMemberRelation(TimeStampedModel):
    meeting = models.ForeignKey('meetings.Meeting', on_delete=models.CASCADE, null=False)
    member = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False)
    MEMBER_MANAGER, MEMBER_STUDENT = 'manager', 'student'
    MEMBER_TYPE_CHOICES = (
        (MEMBER_MANAGER, '관리자'),
        (MEMBER_STUDENT, '학생'),
    )
    member_type = models.CharField(max_length=10, choices=MEMBER_TYPE_CHOICES, null=False)

    class Meta:
        unique_together = [['meeting', 'member'], ]


class Meeting(TimeStampedModel):
    title = models.CharField(max_length=30, default='Untitled')
    description = models.TextField(default='')
    host = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='+')
    members = models.ManyToManyField('users.User', related_name='meetings', through='meetings.MeetingMemberRelation')
    is_ongoing = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Meeting, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
        MeetingMemberRelation.objects.get_or_create(
            member=self.host,
            meeting=self,
            member_type=MeetingMemberRelation.MEMBER_MANAGER
        )

    def get_detail_url(self):
        return reverse_lazy('meeting:detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse_lazy('meeting:update', kwargs={'pk': self.pk})

    def get_start_url(self):
        return reverse_lazy('meeting:start', kwargs={'pk': self.pk})