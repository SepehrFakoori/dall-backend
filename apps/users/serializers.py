from typing import Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")
        read_only_fields = ("username",)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Password is incorrect")
        return value

    def validate_new_password(self, value):
        validate_password(value, self.context["request"].user)
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user


class LoginSerializer(TokenObtainPairSerializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    profile_incomplete = serializers.BooleanField(read_only=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        data: dict[str, Any] = super().validate(attrs)
        data["profile_incomplete"] = not (self.user.first_name and self.user.last_name)
        return data
