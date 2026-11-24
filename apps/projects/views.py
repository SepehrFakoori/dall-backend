from rest_framework import viewsets

from .models import Project, Use
from .serializers import ProjectSerializer, UseSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


class UseViewSet(viewsets.ModelViewSet):
    serializer_class = UseSerializer

    def get_queryset(self):
        return Use.objects.all()
