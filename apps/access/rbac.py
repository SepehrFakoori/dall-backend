from rest_framework.permissions import BasePermission

from .services import get_resolver


class HasRbacPermission(BasePermission):
    """Deny by default: every action must be mapped to a permission code."""

    def _code(self, view):
        return getattr(view, "permission_map", {}).get(view.action)

    def has_permission(self, request, view):
        code = self._code(view)
        return code is not None and get_resolver(request).can(code)

    def has_object_permission(self, request, view, obj):
        code = self._code(view)
        return code is not None and get_resolver(request).can(code, obj)
