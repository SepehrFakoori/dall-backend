from django.db import models

from core.models import SoftDeleteModel
from .organization_manager import OrganizationManager
from .organization_queryset import OrganizationQuerySet


class Organization(SoftDeleteModel):
    name = models.CharField(max_length=255)

    objects = OrganizationManager()
    all_objects = OrganizationQuerySet.as_manager()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
