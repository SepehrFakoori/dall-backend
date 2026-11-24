import uuid
from django.http import JsonResponse
from rest_framework import status

from .services import get_tenant
from .context import set_current_tenant, reset_current_tenant

HEADER = "HTTP_X_TENANT_ID"


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tenant = None
        raw = request.META.get(HEADER)
        token = None

        if raw:
            try:
                tenant_id = uuid.UUID(raw)
            except ValueError:
                return JsonResponse(
                    {"detail": "Tenant not available."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            tenant = get_tenant(tenant_id)
            if tenant is None:
                return JsonResponse(
                    {"detail": "Tenant not available."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            request.tenant = tenant
            token = set_current_tenant(tenant)

        try:
            return self.get_response(request)
        finally:
            if token is not None:
                reset_current_tenant(token)
