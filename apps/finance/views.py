from rest_framework import viewsets

from .models import AccountType, BankAccount
from .serializers import AccountTypeSerializer, BankAccountSerializer


class AccountTypeViewSet(viewsets.ModelViewSet):
    serializer_class = AccountTypeSerializer

    def get_queryset(self):
        return AccountType.objects.all()


class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = BankAccountSerializer

    def get_queryset(self):
        return BankAccount.objects.all()
