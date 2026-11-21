from rest_framework import viewsets

from .models import Bank, CheckType, CheckStatus, Check
from .serializers import (
    BankSerializer,
    CheckSerializer,
    CheckTypeSerializer,
    CheckStatusSerializer,
)


class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer


class CheckTypeViewSet(viewsets.ModelViewSet):
    queryset = CheckType.objects.all()
    serializer_class = CheckTypeSerializer


class CheckStatusViewSet(viewsets.ModelViewSet):
    queryset = CheckStatus.objects.all()
    serializer_class = CheckStatusSerializer


class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
