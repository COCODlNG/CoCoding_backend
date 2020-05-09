from django import forms
from django.forms import ModelMultipleChoiceField

from apps.meetings.models import Meeting
from apps.users.models import User


class MeetingForm(forms.ModelForm):
    members = ModelMultipleChoiceField(queryset=User.objects.all())

    class Meta:
        fields = ['title', 'members']
        model = Meeting
