from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response

from .models import Tenant, Membership
from .serializers import (
    TenantSerializer,
    MembershipSerializer,
    CreatedMembershipSerializer,
    MemberCreateSerializer,
)
from .services import create_tenant_member


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.method not in SAFE_METHODS:
            tenants = Tenant.objects.all()
            if not request.user.is_superuser:
                tenants = tenants.for_user(request.user)
            self.tenant = get_object_or_404(tenants, pk=self.kwargs["tenant_pk"])

    def get_queryset(self):
        tenant_id = self.kwargs["tenant_pk"]
        return super().get_queryset().filter(tenant_id=tenant_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["tenant"] = getattr(self, "tenant", None)
        return context

    @extend_schema(
        responses={status.HTTP_201_CREATED: CreatedMembershipSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="create-user",
        serializer_class=MemberCreateSerializer,
    )
    def create_user(self, request, *args, **kwargs):
        """Create an ERP user and add them as an active tenant member."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            membership = create_tenant_member(
                tenant=self.tenant,
                **serializer.validated_data,
            )
        except DjangoValidationError as exc:
            raise ValidationError(exc.message_dict) from exc
        return Response(
            CreatedMembershipSerializer(membership).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None, **kwargs):
        membership = self.get_object()
        membership.activate()

        return Response(
            self.get_serializer(membership).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None, **kwargs):
        membership = self.get_object()
        membership.deactivate()

        return Response(
            self.get_serializer(membership).data,
            status=status.HTTP_200_OK,
        )
