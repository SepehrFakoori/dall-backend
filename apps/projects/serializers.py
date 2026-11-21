from rest_framework import serializers

from .models import Project, Use


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class UseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Use
        fields = "__all__"
