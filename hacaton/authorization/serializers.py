from rest_framework import serializers
from .models import User
from .exceptions import UserAlreadyExistsError


class UserAuthSerializer(serializers.Serializer):
    username = serializers.RegexField('^[0-9A-z_.]{3,20}$', write_only=True)
    password = serializers.CharField(min_length=8, max_length=128, write_only=True)


class RegistrationSerializer(UserAuthSerializer):
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise UserAlreadyExistsError()
        return value


class TokensSerializer(serializers.Serializer):
    access_token = serializers.UUIDField()
    refresh_token = serializers.UUIDField()

