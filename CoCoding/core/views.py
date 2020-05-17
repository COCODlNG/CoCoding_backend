from django.shortcuts import redirect


class CheckUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('user:login')
        return super(CheckUserMixin, self).dispatch(request, *args, **kwargs)

