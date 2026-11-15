from django.db import models


class UserRole(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_roles",
    )
    role = models.ForeignKey(
        "authorization.Role",
        on_delete=models.CASCADE,
        related_name="user_assignments",
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "role"],
                name="unique_user_role",
            ),
        ]
