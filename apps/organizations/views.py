from rest_framework import viewsets

from .models import (
    Organization,
    OrganizationMembership,
    Department,
    DepartmentMembership,
)
from .serializers import (
    OrganizationSerializer,
    OrganizationMembershipSerializer,
    DepartmentSerializer,
    DepartmentMembershipSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationMembershipViewSet(viewsets.ModelViewSet):
    # queryset = OrganizationMembership.objects.all()
    serializer_class = OrganizationMembershipSerializer

    def get_queryset(self):
        return OrganizationMembership.objects.filter(
            organization_id=self.kwargs["organization_pk"]
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
