from django.db import models

from apps.projects.models import ProjectScopedModel
from core.models import ScopedSerialModel


class FloorType(ProjectScopedModel, ScopedSerialModel):
    serial_prefix = "FT"
    serial_scope_field = "project"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Floor(ProjectScopedModel, ScopedSerialModel):
    serial_prefix = "FLR"
    serial_scope_field = "project"

    block = models.ForeignKey(
        "technical.Block",
        on_delete=models.CASCADE,
        related_name="floors",
    )
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    type = models.ForeignKey(
        FloorType,
        on_delete=models.CASCADE,
        related_name="floors",
    )
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name
