from django.db import models
from django.conf import settings

from .organization_membership_queryset import OrganizationMembershipQuerySet


class OrganizationMembership(models.Model):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="memberships",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="organization_memberships",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = OrganizationMembershipQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "user"],
                name="unique_organization_membership",
            )
        ]

    def __str__(self) -> str:
        return f"{self.organization} - {self.user}"
