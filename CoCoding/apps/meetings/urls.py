from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.meetings import views

router = DefaultRouter(trailing_slash=False)
router.register('meetings', views.MeetingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]