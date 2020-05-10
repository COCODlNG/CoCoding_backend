from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import RedirectView, CreateView

from .forms import UserCreationForm

from core.views import CheckUserMixin


class LoginView(BaseLoginView):
    template_name = 'login.html'

    def get_redirect_url(self):
        return reverse_lazy('meeting:list')


class LogoutView(CheckUserMixin, RedirectView):
    url = reverse_lazy('index')

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)


class UserRegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
