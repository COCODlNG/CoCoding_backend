from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet

from apps.meetings.models import Meeting
from apps.users.models import User
from apps.meetings.serializers import MeetingDetailSerializer, MeetingMemberRelationSerializer


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
    queryset = User.objects.all().order_by('id')
