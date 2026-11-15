from rest_framework.permissions import BasePermission

from .services.permission_checker import has_permission


class HasRBPermission(BasePermission):
    def has_permission(self, request, view):
        permission_map = getattr(
            view,
            "required_permissions",
            {},
        )

        permission_code = permission_map.get(view.action)

        if not permission_code:
            return False

        return has_permission(request.user, permission_code)
