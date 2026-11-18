from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class OrganizationPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.method != "POST"
            or request.user.has_perm("organizations.add_organization")
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.memberships.filter(
            user=request.user,
            is_active=True,
            is_admin=True,
        ).exists()
