import uuid

from django.db import models
from django_tenants.models import TenantMixin

from core.models import TimeStampedModel
from .querysets import TenantQuerySet


class Tenant(TenantMixin, TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    auto_create_schema = True  # creates the schema and runs migrations on save()

    objects = TenantQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self) -> str:
        return self.name
