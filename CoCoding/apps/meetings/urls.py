from django.urls import path

from apps.meetings.views import MeetingCreateView, MeetingUpdateView, MeetingDetailView, MeetingListView, \
    MeetingStartView, MeetingMemberUpdateView

urlpatterns = [
    path('', MeetingListView.as_view(), name='list'),
    path('create/', MeetingCreateView.as_view(), name='create'),
    path('<int:pk>/', MeetingDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', MeetingUpdateView.as_view(), name='update'),
    path('<int:pk>/start/', MeetingStartView.as_view(), name='start'),
    path('<int:pk>/member_update/', MeetingMemberUpdateView.as_view(), name='member_update'),

]
