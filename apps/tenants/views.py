from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from .models import Tenant, Membership
from .serializers import (
    CurrentTenantSerializer,
    MembershipSerializer,
    CreatedMembershipSerializer,
    MemberCreateSerializer,
)
from .services import create_tenant_member


class CurrentTenantView(RetrieveUpdateAPIView):
    http_method_names = ["get", "patch", "head", "options"]  # no full PUT
    serializer_class = CurrentTenantSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return self.request.tenant

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        super().update(request, *args, **kwargs)
        return Response(self.get_serializer(self.get_object()).data)


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

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
                tenant=self.request.tenant,
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
