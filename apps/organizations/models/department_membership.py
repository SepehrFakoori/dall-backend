from django.db import models


class DepartmentMembership(models.Model):
    membership = models.ForeignKey(
        "tenants.Membership",
        on_delete=models.CASCADE,
        related_name="departments",  # department_memberships
    )
    department = models.ForeignKey(
        "organizations.Department",
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
