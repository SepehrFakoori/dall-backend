from collections.abc import Mapping

from rest_framework import serializers

from apps.users.serializers import UserSerializer
from apps.users.models import User
from ..models import Membership


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


class CreatedMembershipSerializer(MembershipSerializer):
    user = UserSerializer(read_only=True)


class MemberCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name")
        extra_kwargs = {
            "first_name": {"required": False, "allow_blank": True},
            "last_name": {"required": False, "allow_blank": True},
        }

    def to_internal_value(self, data):
        if isinstance(data, Mapping) and isinstance(data.get("username"), str):
            data = data.copy()
            data["username"] = User.normalize_username(data["username"])
        return super().to_internal_value(data)
