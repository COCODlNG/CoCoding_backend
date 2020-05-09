from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'password', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }
