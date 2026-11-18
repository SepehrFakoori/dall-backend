from django.conf import settings
from django.db import models


class DepartmentMembership(models.Model):
    department = models.ForeignKey(
        "organizations.Department",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="Departments",  # department_memberships
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "department"],
                name="unique_org_membership",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} @ {self.department}"
