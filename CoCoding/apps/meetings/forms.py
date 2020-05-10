from django import forms

from apps.meetings.models import Meeting


class MeetingForm(forms.ModelForm):

    class Meta:
        fields = ['title', 'description']
        model = Meeting
