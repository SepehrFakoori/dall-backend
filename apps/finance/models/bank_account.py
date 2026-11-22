from django.db import models

from apps.organizations.models import OrganizationScopedModel


class AccountType(OrganizationScopedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class BankAccount(OrganizationScopedModel):
    bank_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=20, unique=True)
    iban = models.CharField(max_length=24, unique=True)
    account_type = models.ForeignKey(
        AccountType, on_delete=models.PROTECT, related_name="bank_accounts"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "account_number", "iban"],
                name="unique_bank_account_per_organization",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.account_number} @ {self.bank_name}"
