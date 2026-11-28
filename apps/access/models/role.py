from django.db import models
from rest_framework.exceptions import ValidationError

from core.models import TimeStampedModel
from ..register import get_permission


class Role(TimeStampedModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_system = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_role_name",
            ),
        ]

    def activate(self) -> None:
        if self.is_active:
            return

        self.is_active = True
        self.save(update_fields=["is_active", "updated_at"])

    def deactivate(self) -> None:
        if not self.is_active:
            return

        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])

    def __str__(self) -> str:
        return self.name


class Scope(models.TextChoices):
    ALL = "all"
    OWN = "own"


class RolePermission(TimeStampedModel):
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="permissions",
    )
    code = models.CharField(max_length=100)
    scope = models.CharField(
        max_length=10,
        choices=Scope.choices,
        default=Scope.ALL,
    )

    def clean(self) -> None:
        perm = get_permission(self.code)
        if perm is None:
            raise ValidationError({"code": "Unknown permission code."})
        if not perm.scoped and self.scope != Scope.ALL:
            raise ValidationError(
                {"scope": "This permission does not support a scope."}
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()  # make sure invalid rows can't be saved from code either
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.role} . {self.code} ({self.scope})"


class RoleAssignment(TimeStampedModel):
    membership = models.ForeignKey(
        "tenants.Membership",
        on_delete=models.DO_NOTHING,
        related_name="role_assignments",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="assignments",
    )
    department = models.ForeignKey(
        "organization.Department",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="role_assignments",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["membership", "role", "department"],
                condition=models.Q(department__isnull=False),
                name="unique_assigment_department",
            ),
            models.UniqueConstraint(
                fields=["membership", "role"],
                condition=models.Q(department__isnull=True),
                name="unique_assigment_tenant",
            ),
        ]
