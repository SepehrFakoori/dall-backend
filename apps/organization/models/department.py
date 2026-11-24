from django.db import models

from apps.tenants.models import TenantScopeModel


class Department(TenantScopeModel):
    name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name", "pk"]

    def activate(self) -> None:
        if self.is_active:
            return

        self.is_active = True
        self.save(update_fields=["is_active"])

    def deactivate(self) -> None:
        if not self.is_active:
            return

        self.is_active = False
        self.save(update_fields=["is_active"])

    def __str__(self) -> str:
        return f"{self.name} @ {self.tenant}"
