from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Permission, Role, UserRole
from .serializers import PermissionSerializer, RoleSerializer, UserRoleSerializer
from .permissions import HasRBPermission


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    required_permissions = {
        "list": "permissions.view",
        "retrieve": "permissions.view",
        "create": "permissions.create",
        "update": "permissions.update",
        "partial_update": "permissions.update",
        "destroy": "permissions.delete",
    }


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, HasRBPermission]

    required_permissions = {
        "list": "roles.view",
        "retrieve": "roles.view",
        "create": "roles.create",
        "update": "roles.update",
        "partial_update": "roles.update",
        "destroy": "roles.delete",
    }


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

    required_permissions = {
        "list": "user_roles.view",
        "retrieve": "user_roles.view",
        "create": "user_roles.create",
        "update": "user_roles.update",
        "partial_update": "user_roles.update",
        "destroy": "user_roles.delete",
    }

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        user_roles = UserRole.objects.filter(user=request.user).select_related(
            "user", "role"
        )
        serializer = self.get_serializer(user_roles, many=True)
        return Response(serializer.data)
