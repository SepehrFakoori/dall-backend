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
    serializer_class = AccountTypeSerializer

    def get_queryset(self):
        return AccountType.objects.all()


class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = BankAccountSerializer

    def get_queryset(self):
        return BankAccount.objects.all()


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
