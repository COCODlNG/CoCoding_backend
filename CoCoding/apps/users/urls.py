from django.urls import path
from .views import LoginView, LogoutView, UserRegisterView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', UserRegisterView.as_view(), name='signup'),
]
