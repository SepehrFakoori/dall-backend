from rest_framework import serializers

from . import PermissionSerializer
from ..models.role import Role


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = "__all__"
