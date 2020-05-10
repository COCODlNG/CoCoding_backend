from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, RedirectView, DetailView

from apps.meetings.forms import MeetingForm
from apps.meetings.models import Meeting, MeetingMemberRelation
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
