from django.db import models

from core.models import TimeStampedModel


class DepartmentMembership(TimeStampedModel):
    membership = models.ForeignKey(
        "tenants.Membership",
        on_delete=models.CASCADE,
        related_name="departments",  # department_memberships
    )
    department = models.ForeignKey(
        "organization.Department",
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["membership", "department"],
                name="unique_department_membership",
            )
        ]

    def __str__(self) -> str:
        return f"{self.membership} @ {self.department}"
