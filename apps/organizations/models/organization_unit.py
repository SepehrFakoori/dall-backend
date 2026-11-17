from django.db import models

from .organization_unit_queryset import OrganizationUnitQuerySet


class OrganizationUnit(models.Model):
    class Type(models.TextChoices):
        DEPARTMENT = "department"
        LINE = "line"

    name = models.CharField(max_length=100)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="units",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.DEPARTMENT,
    )

    objects = OrganizationUnitQuerySet.as_manager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(type="department", parent__isnull=True)
                    | models.Q(type="line", parent__isnull=False)
                ),
                name="valid_unit_parent_type",
            ),
        ]

    def __str__(self) -> str:
        return self.name
