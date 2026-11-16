from django.core.exceptions import ValidationError
from django.db import models


class UnitMembership(models.Model):
    membership = models.ForeignKey(
        "organizations.OrganizationMembership",
        on_delete=models.CASCADE,
        related_name="unit_membership",
    )
    unit = models.ForeignKey(
        "organizations.OrganizationUnit",
        on_delete=models.PROTECT,
        related_name="unit_membership",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["membership", "unit"],
                name="unique_unit_member",
            )
        ]

    def clean(self) -> None:
        super().clean()
        if self.membership and self.unit:
            if self.membership.organization_id != self.unit.organization_id:
                raise ValidationError(
                    "Membership and unit must belong to the same organization."
                )

    def __str__(self) -> str:
        return f"{self.membership} - {self.unit}"
