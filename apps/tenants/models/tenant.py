import uuid

from django.db import models

from core.models import TimeStampedModel
from .querysets import TenantQuerySet
from ..context import get_current_tenant


class Tenant(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    objects = TenantQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self) -> str:
        return self.name


class TenantManager(models.Manager):
    def get_queryset(self):
        tenant = get_current_tenant()
        if tenant is None:
            raise RuntimeError("No tenant in context.")
        return super().get_queryset().filter(tenant=tenant)


class TenantScopeModel(models.Model):
    """
    Base models for Tenant Scope.
    """

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="+",
        editable=False,
    )

    objects = TenantManager()
    unscoped = models.Manager()
    # objects = TenantScopedQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding and self.tenant_id is None:
            tenant = get_current_tenant()
            if tenant is None:
                raise RuntimeError("No tenant in context.")
            self.tenant = tenant
        super().save(*args, **kwargs)
