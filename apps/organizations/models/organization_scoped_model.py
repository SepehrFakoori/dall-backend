from django.db import models

from .querysets import OrganizationScopedQuerySet


class OrganizationScopedModel(models.Model):
    """
    Base model for records owned by exactly one organization.
    """

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="+",
    )

    objects = OrganizationScopedQuerySet.as_manager()

    class Meta:
        abstract = True
