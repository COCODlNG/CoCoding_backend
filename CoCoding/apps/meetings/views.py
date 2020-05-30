from django.http import HttpResponseForbidden, JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, RedirectView, DetailView, View
from django.views.generic.edit import BaseUpdateView, DeleteView
from django.contrib import messages
from apps.meetings.forms import MeetingForm
from apps.meetings.models import Meeting, MeetingMemberRelation
from apps.users.models import User
from core.views import CheckUserMixin


class MeetingListView(CheckUserMixin, ListView):
    model = Meeting
    template_name = 'meeting_list.html'

    def get_queryset(self):
        return self.request.user.meetings.all()


class MeetingUpdateView(CheckUserMixin, UpdateView):
    model = Meeting
    template_name = 'meeting_form.html'
    form_class = MeetingForm

    success_url = reverse_lazy('meeting:list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.url_hash is None:
            self.object.url_hash = self.object.pk
            self.object.save()
        return super(BaseUpdateView, self).get(request, *args, **kwargs)


class MeetingCreateView(CheckUserMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        meeting = Meeting(host=self.request.user)
        meeting.save()
        return reverse_lazy('meeting:update', kwargs={'pk': meeting.pk})


class MeetingDetailView(CheckUserMixin, DetailView):
    model = Meeting
    template_name = 'meeting_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not MeetingMemberRelation.objects.filter(meeting=self.object, member=self.request.user).exists():
            return HttpResponseForbidden()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class MeetingStartView(CheckUserMixin, RedirectView):
    meeting = None

    def setup(self, request, *args, **kwargs):
        super(MeetingStartView, self).setup(request, *args, **kwargs)
        self.meeting = get_object_or_404(Meeting, pk=kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        if self.request.user == self.meeting.host:
            self.meeting.is_ongoing = True
            self.meeting.save(update_fields=['is_ongoing'])
        else:
            return HttpResponseForbidden()
        return super(MeetingStartView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('meeting:detail', kwargs={'pk': self.meeting.id})


class MeetingDeleteView(CheckUserMixin, DeleteView):

    model = Meeting
    success_url = reverse_lazy('meeting:list')
    meeting = None

    def get(self, request, *args, **kwargs):
        self.meeting = get_object_or_404(Meeting, pk=kwargs['pk'])
        if self.request.user == self.meeting.host:
            return self.post(request, *args, **kwargs)
        else:
            return reverse_lazy('meeting:list')


class MeetingMemberUpdateView(View):

    pk_url_kwarg = 'pk'
    meeting = None
    user = None

    def post(self, request, *args, **kwargs):
        username = request.POST.get('id_member')

        self.user = get_object_or_404(User, username=username)
        self.meeting = get_object_or_404(Meeting, pk=kwargs['pk'])
        try:
            MeetingMemberRelation.objects.create(meeting=self.meeting, member=self.user)
        except Exception:
            context = {
                'message': 'unique',
                'error': '이미 추가한 아이디입니다.',
            }
            return JsonResponse(context, json_dumps_params={'ensure_ascii': True})
        context = {
            'user_id': self.user.id,
            'user_name': self.user.username,
            'user_type': '학생',
            }
        return JsonResponse(context, json_dumps_params={'ensure_ascii': True})


class MeetingMemberDeleteView(View):

    pk_url_kwarg = 'pk'
    meeting = None
    user = None

    def post(self, request, *args, **kwargs):

        user_pk = request.POST.get('delete_id')

        self.user = get_object_or_404(User, pk=user_pk)
        self.meeting = get_object_or_404(Meeting, pk=kwargs['pk'])
        try:
            MeetingMemberRelation.objects.filter(meeting=self.meeting, member=self.user).delete()
        except Exception:
            context = {
                'message': 'already',
                'error': '이미 삭제한 아이디입니다.',
            }
            return JsonResponse(context, json_dumps_params={'ensure_ascii': True})
        return HttpResponse(status=200)


class InvitationRedirectView(CheckUserMixin, RedirectView):

    meeting = None
    meeting_relation = None

    def setup(self, request, *args, **kwargs):
        super(InvitationRedirectView, self).setup(request, *args, **kwargs)
        self.meeting = get_object_or_404(Meeting, url_hash=kwargs['hash'])

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            hash_value = str(kwargs['hash'])
            login_url = reverse('user:login')
            return redirect(login_url + '?hash=' + hash_value)

        try:
            MeetingMemberRelation.objects.create(meeting=self.meeting, member=self.request.user)
        except Exception:
            messages.add_message(self.request, messages.WARNING, '이미 참가하고 있는 미팅입니다.')
            return HttpResponseRedirect(reverse_lazy('meeting:list'))

        return super(InvitationRedirectView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, '이제 미팅에 참여 할 수 있습니다.')
        return reverse_lazy('meeting:list')
