from rest_framework import viewsets

from .filters import CheckFilter
from .models import CheckType, CheckStatus, Check
from .serializers import CheckSerializer, CheckTypeSerializer, CheckStatusSerializer


class CheckTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CheckTypeSerializer

    def get_queryset(self):
        return CheckType.objects.all()


class CheckStatusViewSet(viewsets.ModelViewSet):
    serializer_class = CheckStatusSerializer

    def get_queryset(self):
        return CheckStatus.objects.all()


class CheckViewSet(viewsets.ModelViewSet):
    serializer_class = CheckSerializer
    filterset_class = CheckFilter

    def get_queryset(self):
        return Check.objects.select_related("type")
