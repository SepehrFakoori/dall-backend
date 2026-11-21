from rest_framework import serializers

from ..models import Check, CheckType, CheckStatus


class CheckTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckType
        fields = "__all__"


class CheckStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckStatus
        fields = "__all__"


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = "__all__"
