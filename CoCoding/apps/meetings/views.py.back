from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.meetings.models import Meeting
from apps.meetings.serializers import MeetingDetailSerializer, MeetingMemberRelationSerializer
from apps.meetings.models import MeetingMemberRelation


class MeetingViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):

    serializer_class = MeetingDetailSerializer
    queryset = Meeting.objects.all()

    def get_queryset(self):
        return self.request.user.meetings.all()


class MeetingMemberViewSet(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):

    serializer_class = MeetingMemberRelationSerializer
    queryset = MeetingMemberRelation.objects.all()

    def get_queryset(self):
        queryset = super(MeetingMemberViewSet, self).get_queryset()
        meeting_pk = self.kwargs.get('meeting_pk')
        if meeting_pk:
            queryset.filter(meeting=meeting_pk)
        return queryset
