from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.meetings.views import MeetingMemberViewSet, MeetingViewSet

router = DefaultRouter(trailing_slash=False)
router.register('meetings', MeetingViewSet)
router.register('meetings/create', MeetingMemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
]