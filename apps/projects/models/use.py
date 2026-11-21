from django.db import models

from apps.organizations.models import OrganizationScopedModel


class Use(OrganizationScopedModel):
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="unique_use_per_organization",
            ),
        ]

    def __str__(self) -> str:
        return self.name
