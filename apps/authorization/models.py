from django.db import models
from django.db.models.query_utils import Q

from apps.tenants.models import TenantScopeModel


class Permission(models.Model):
    codename = models.CharField(max_length=100, unique=True)
    module = models.CharField(max_length=50)
    label = models.CharField(max_length=150)
    description = models.BooleanField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.codename


class Role(TenantScopeModel):
    name = models.CharField(max_length=100)
    code = models.SlugField(max_length=50, blank=True)
    is_system = models.BooleanField(default=False)
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="roles",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "name"],
                name="unique_role_tenant_name",
            ),
            models.UniqueConstraint(
                fields=["tenant", "code"],
                condition=~Q(code=""),
                name="unique_role_tenant_code",
            ),
        ]

    def __str__(self) -> str:
        return self.name


class RoleAssignment(models.Model):
    membership = models.ForeignKey("tenants.Membership", on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    scope_type = models.CharField(max_length=20, default="tenant")
    scope_id = models.PositiveIntegerField(null=True, blank=True)
