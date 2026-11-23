from django.db import models

from .querysets import TenantQuerySet, TenantScopedQuerySet


class Tenant(models.Model):
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TenantQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self) -> str:
        return self.name


class TenantScopeModel(models.Model):
    """
    Base models for Tenant Scope.
    """

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="+",
    )

    objects = TenantScopedQuerySet.as_manager()

    class Meta:
        abstract = True
