from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Membership(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "tenant"],
                name="unique_membership",
            )
        ]

    def activate(self) -> None:
        if self.is_active:
            return

        self.is_active = True
        self.save(update_fields=["is_active", "updated_at"])

    def deactivate(self) -> None:
        if not self.is_active:
            return

        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])

    def __str__(self) -> str:
        return f"{self.user} @ {self.tenant}"
