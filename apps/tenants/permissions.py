from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException

from .models import Membership


class TenantRequired(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "X-Tenant-ID header is required."


class IsTenantMember(BasePermission):
    message = "Tenant not available."

    def has_permission(self, request, view):
        if not getattr(view, "tenant_required", True):
            return True
        tenant = getattr(request, "tenant", None)
        if tenant is None:
            raise TenantRequired()

        user = request.user
        if not (user and user.is_authenticated):
            return False

        return Membership.objects.filter(
            user=user,
            tenant=tenant,
            is_active=True,
        )
