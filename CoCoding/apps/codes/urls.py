from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CodeViewSet


router = DefaultRouter()
router.register('', CodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]