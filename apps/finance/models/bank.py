from django.db import models

from apps.organizations.models import OrganizationScopedModel


class Bank(OrganizationScopedModel):
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "account_number"],
                name="unique_bank_account_per_organization",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.account_number} @ {self.name}"
