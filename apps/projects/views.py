from rest_framework import viewsets

from .models import Project, Use
from .serializers import ProjectSerializer, UseSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class UseViewSet(viewsets.ModelViewSet):
    queryset = Use.objects.all()
    serializer_class = UseSerializer
