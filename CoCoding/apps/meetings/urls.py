from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.meetings.views import MeetingMemberViewSet, MeetingViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', MeetingViewSet)
meeting_member_list = MeetingMemberViewSet.as_view({'get': 'list'})
add_meeting_member = MeetingMemberViewSet.as_view({'post': 'create'})
delete_meeting_member = MeetingMemberViewSet.as_view({'post': 'destroy'})

urlpatterns = [
    path('', include(router.urls)),
    path('<int:meeting_pk>/members', meeting_member_list),
    path('<int:meeting_pk>/members', add_meeting_member),
    path('members/<int:pk>/delete', delete_meeting_member),
]
