from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import LoginView, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('meetings/', include(router.urls)),
]
