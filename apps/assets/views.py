from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Asset
from .serializers import AssetSerializer
from ..authorization.permissions import HasRBPermission


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated, HasRBPermission]

    required_permissions = {
        "list": "assets.view",
        "retrieve": "assets.view",
        "create": "assets.create",
        "update": "assets.update",
        "partial_update": "assets.update",
        "destroy": "assets.delete",
    }
