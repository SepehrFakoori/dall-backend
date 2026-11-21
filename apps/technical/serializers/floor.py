from rest_framework import serializers

from ..models import Floor, FloorType


class FloorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorType
        fields = "__all__"


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = "__all__"
