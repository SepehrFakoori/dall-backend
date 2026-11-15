from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .serializers import ProjectSerializer
from ..authorization.permissions import HasRBPermission


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, HasRBPermission]

    required_permissions = {
        "list": "projects.view",
        "retrieve": "projects.view",
        "create": "projects.create",
        "update": "projects.update",
        "partial_update": "projects.update",
        "destroy": "projects.delete",
    }
