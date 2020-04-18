from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.meetings.models import Meeting
from apps.meetings.serializers import MeetingDetailSerializer, MeetingMemberRelationSerializer
from apps.users.models import User


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
