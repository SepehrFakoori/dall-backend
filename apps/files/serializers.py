from rest_framework import serializers

from .models import File
from .services import get_download_url


class CreateUploadSerializer(serializers.Serializer):
    purpose = serializers.CharField(max_length=100)
    filename = serializers.CharField(max_length=255)
    content_type = serializers.CharField(max_length=100)
    size = serializers.IntegerField(min_value=1)


class FileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = "__all__"
        read_only_fields = fields

    def get_url(self, obj):
        return get_download_url(obj)
