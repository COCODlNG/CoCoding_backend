from django.contrib import admin
from apps.meetings.models import Meeting, MeetingMemberRelation


admin.site.register(Meeting)
admin.site.register(MeetingMemberRelation)