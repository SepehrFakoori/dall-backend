from django.db import models

from apps.organizations.models import OrganizationScopedModel


class Bank(OrganizationScopedModel):
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"{self.account_number} @ {self.name}"
