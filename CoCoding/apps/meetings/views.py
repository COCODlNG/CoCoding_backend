from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Meeting
from .serializers import MeetingDetailSerializer


class MeetingViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):

    serializer_class = MeetingDetailSerializer
    queryset = Meeting.objects.all()

    def get_queryset(self):
        return self.request.user.meetings.all()
