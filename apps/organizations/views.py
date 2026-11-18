from rest_framework import viewsets

from .models import Organization, OrganizationMembership
from .serializers import OrganizationSerializer, OrganizationMembershipSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationMemberShipViewSet(viewsets.ModelViewSet):
    queryset = OrganizationMembership.objects.all()
    serializer_class = OrganizationMembershipSerializer
