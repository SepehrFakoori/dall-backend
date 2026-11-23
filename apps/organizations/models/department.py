from django.db import models

from apps.tenants.models import TenantScopeModel


class Department(TenantScopeModel):
    name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name", "pk"]

    def __str__(self) -> str:
        return f"{self.name} @ {self.tenant}"
