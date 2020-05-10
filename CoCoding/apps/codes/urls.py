from django.urls import path

from apps.codes.views import run_code

urlpatterns = [
    path('run/', run_code, name='run'),
]
