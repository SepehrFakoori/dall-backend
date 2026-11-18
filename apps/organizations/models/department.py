from django.db import models

from .organization_scoped_model import OrganizationScopedModel


class Department(OrganizationScopedModel):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name", "pk"]

    def __str__(self) -> str:
        return self.name
