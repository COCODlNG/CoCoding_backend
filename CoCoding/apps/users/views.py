from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import RedirectView, CreateView

from .forms import UserCreationForm


class LoginView(BaseLoginView):
    template_name = 'login.html'
    context_hash = None
    hash_value = None

    def get_redirect_url(self):
        self.context_hash = self.request.GET.get('hash')
        self.hash_value = self.request.POST.get('hash')
        if self.context_hash:
            self.extra_context = {'hash': self.context_hash}
        if self.hash_value:
            return reverse_lazy('meeting:invitation', kwargs={'hash': self.hash_value})
        return reverse_lazy('meeting:list')


class LogoutView(RedirectView):
    url = reverse_lazy('index')

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)


class UserRegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('user:login')

