from rest_framework import serializers

from .models import Organization, OrganizationMembership, OrganizationUnit


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationMembershipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMembership
        fields = "__all__"


class OrganizationUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationUnit
        fields = "__all__"
