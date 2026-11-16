from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Organization, OrganizationMembership, OrganizationUnit
from .serializers import (
    OrganizationSerializer,
    OrganizationMembershipsSerializer,
    OrganizationUnitsSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (AllowAny,)


class OrganizationMembershipsViewSet(viewsets.ModelViewSet):
    queryset = OrganizationMembership.objects.all()
    serializer_class = OrganizationMembershipsSerializer
    permission_classes = (AllowAny,)


class OrganizationUnitsViewSet(viewsets.ModelViewSet):
    queryset = OrganizationUnit.objects.all()
    serializer_class = OrganizationUnitsSerializer
    permission_classes = (AllowAny,)
