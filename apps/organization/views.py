from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import DepartmentSerializer, DepartmentMembershipSerializer
from .models import Department, DepartmentMembership


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.all()

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        department = self.get_object()
        department.activate()

        return Response(
            self.get_serializer(department).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        department = self.get_object()
        department.deactivate()

        return Response(
            self.get_serializer(department).data,
            status=status.HTTP_200_OK,
        )


class DepartmentMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentMembershipSerializer

    def get_queryset(self):
        return DepartmentMembership.objects.filter(
            department_id=self.kwargs["department_pk"]
        )
