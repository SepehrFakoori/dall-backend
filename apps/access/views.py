from rest_framework import viewsets

from .models import Role
from .serializers import RoleSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer()
    permission_map = {
        "list": "role.view",
        "retrieve": "role.view",
        "create": "role.manage",
        "partial_update": "role.manage",
        "destroy": "role.manage",
    }
