from rest_framework import serializers

from ..models import ProjectProfile


class ProjectProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectProfile
        fields = "__all__"
