from rest_framework import serializers

from ..models import DepartmentMembership


class DepartmentMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentMembership
        fields = ["id", "department", "membership"]
