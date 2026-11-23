from rest_framework import viewsets

from .filters import CheckFilter
from .models import AccountType, BankAccount, CheckType, CheckStatus, Check
from .serializers import (
    AccountTypeSerializer,
    BankAccountSerializer,
    CheckSerializer,
    CheckTypeSerializer,
    CheckStatusSerializer,
)


class AccountTypeViewSet(viewsets.ModelViewSet):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer


class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


class CheckTypeViewSet(viewsets.ModelViewSet):
    queryset = CheckType.objects.all()
    serializer_class = CheckTypeSerializer


class CheckStatusViewSet(viewsets.ModelViewSet):
    queryset = CheckStatus.objects.all()
    serializer_class = CheckStatusSerializer


class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.select_related("type")
    serializer_class = CheckSerializer
    filterset_class = CheckFilter
