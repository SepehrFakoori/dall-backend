from django.db import models


class RolePermission(models.Model):
    role = models.ForeignKey(
        "Role",
        on_delete=models.CASCADE,
        related_name="role_permissions",
    )

    permission = models.ForeignKey(
        "Permission",
        on_delete=models.CASCADE,
        related_name="role_permissions",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["role", "permission"],
                name="unique_role_permission",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.role.code} - {self.permission.code}"
