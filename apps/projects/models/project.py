from django.db import models

from core.models import SoftDeleteModel, SerialModel


class Project(SoftDeleteModel, SerialModel):
    serial_prefix = "PRJ"

    class Status(models.TextChoices):
        DESIGN = "design"
        PERMITTING = "permitting"
        CONSTRUCTION = "construction"
        COMPLETED = "completed"
        OPERATING = "operating"
        ARCHIVED = "archived"

    name = models.CharField(max_length=255)
    internal_name = models.CharField(max_length=255, blank=True)

    asset = models.ForeignKey(
        "assets.Asset",
        on_delete=models.CASCADE,
        related_name="projects",
    )
    usages = models.ManyToManyField(
        "projects.ProjectUsage",
        related_name="projects",
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DESIGN,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name
