from collections.abc import Mapping

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User
from apps.users.serializers import UserSerializer
from ..models import OrganizationMembership


class OrganizationMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMembership
        fields = ["id", "organization", "user"]

    def validate_organization(self, organization):
        route_organization = self.context.get("organization")
        if route_organization is not None and organization != route_organization:
            raise serializers.ValidationError(_("Use the organization from the URL."))
        return organization


class CreatedOrganizationMembershipSerializer(OrganizationMembershipSerializer):
    user = UserSerializer(read_only=True)


class OrganizationMemberCreateSerializer(serializers.ModelSerializer):
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
