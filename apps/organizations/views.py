from rest_framework import viewsets

from .serializers import DepartmentSerializer, DepartmentMembershipSerializer
from .models import Department, DepartmentMembership


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.for_tenant(tenant_id=self.kwargs["tenant_pk"])


class DepartmentMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentMembershipSerializer

    def get_queryset(self):
        return DepartmentMembership.objects.filter(
            department_id=self.kwargs["department_pk"]
        )
