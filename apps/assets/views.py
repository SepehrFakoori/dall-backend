from rest_framework import viewsets

from .models import Asset
from .serializers import AssetSerializer


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_map = {
        "list": "assets.view",
        "retrieve": "assets.view",
        "create": "assets.manage",
        "partial_update": "assets.manage",
        "destroy": "assets.manage",
    }
