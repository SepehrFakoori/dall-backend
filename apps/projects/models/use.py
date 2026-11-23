from django.db import models

from apps.tenants.models import TenantScopeModel


class Use(TenantScopeModel):
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "name"],
                name="unique_use_per_tenant",
            ),
        ]

    def __str__(self) -> str:
        return self.name
