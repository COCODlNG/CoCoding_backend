from rest_framework import serializers
from .models import Meeting


class MeetingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = (
            'title',
            'host',
        )


class MeetingDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = (
            'title',
            'host',
            'members',
        )
