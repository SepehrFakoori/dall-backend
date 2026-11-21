from django.core.exceptions import ValidationError as DjangoValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import (
    Organization,
    OrganizationMembership,
    Department,
    DepartmentMembership,
)
from .serializers import (
    CreatedOrganizationMembershipSerializer,
    OrganizationMemberCreateSerializer,
    OrganizationSerializer,
    OrganizationMembershipSerializer,
    DepartmentSerializer,
    DepartmentMembershipSerializer,
)
from .services import create_organization_member


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationMembershipViewSet(viewsets.ModelViewSet):
    queryset = OrganizationMembership.objects.all()
    serializer_class = OrganizationMembershipSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.method not in SAFE_METHODS:
            organizations = Organization.objects.all()
            if not request.user.is_superuser:
                organizations = organizations.for_user(request.user)
            self.organization = get_object_or_404(
                organizations, pk=self.kwargs["organization_pk"]
            )

    def get_queryset(self):
        organization_id = self.kwargs["organization_pk"]
        return super().get_queryset().filter(organization_id=organization_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["organization"] = getattr(self, "organization", None)
        return context

    @extend_schema(
        responses={status.HTTP_201_CREATED: CreatedOrganizationMembershipSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="create-user",
        serializer_class=OrganizationMemberCreateSerializer,
    )
    def create_user(self, request, *args, **kwargs):
        """Create an ERP user and add them as an active organization member."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            membership = create_organization_member(
                organization=self.organization,
                **serializer.validated_data,
            )
        except DjangoValidationError as exc:
            raise ValidationError(exc.message_dict) from exc
        return Response(
            CreatedOrganizationMembershipSerializer(membership).data,
            status=status.HTTP_201_CREATED,
        )


class DepartmentViewSet(viewsets.ModelViewSet):
    # queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.for_organization(
            organization_id=self.kwargs["organization_pk"]
        )


class DepartmentMembershipViewSet(viewsets.ModelViewSet):
    # queryset = DepartmentMembership.objects.all()
    serializer_class = DepartmentMembershipSerializer

    def get_queryset(self):
        return DepartmentMembership.objects.filter(
            department_id=self.kwargs["department_pk"]
        )
