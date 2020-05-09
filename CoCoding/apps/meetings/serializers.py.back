from rest_framework import serializers
from .models import Meeting, MeetingMemberRelation
from apps.users.serializers import UserSerializer


class MeetingDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = ['title', 'host', ]


class MeetingMemberRelationSerializer(serializers.ModelSerializer):

    member = UserSerializer()

    class Meta:
        model = MeetingMemberRelation
        fields = ['member', 'member_type']
