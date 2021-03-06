from django.urls import path

from apps.meetings.views import MeetingCreateView, MeetingUpdateView, MeetingDetailView, MeetingListView, \
    MeetingStartView, MeetingMemberUpdateView, MeetingMemberDeleteView, InvitationRedirectView, MeetingDeleteView, \
    MeetingMemberTypeUpdateView

urlpatterns = [
    path('', MeetingListView.as_view(), name='list'),
    path('create/', MeetingCreateView.as_view(), name='create'),
    path('<int:pk>/', MeetingDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', MeetingUpdateView.as_view(), name='update'),
    path('<int:pk>/start/', MeetingStartView.as_view(), name='start'),
    path('<int:pk>/delete/', MeetingDeleteView.as_view(), name='delete'),
    path('<int:pk>/member_update/', MeetingMemberUpdateView.as_view(), name='member_update'),
    path('<int:pk>/member_delete/', MeetingMemberDeleteView.as_view(), name='member_delete'),
    path('<int:pk>/member_type_update/', MeetingMemberTypeUpdateView.as_view(), name='member_type_update'),
    path('invite/<hash>/', InvitationRedirectView.as_view(), name='invitation'),
]
