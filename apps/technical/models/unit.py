from django.db import models

from apps.projects.models import ProjectScopedModel
from core.models import ScopedSerialModel


class Unit(ProjectScopedModel, ScopedSerialModel):
    serial_prefix = "UNIT"
    serial_scope_field = "project"

    number = models.CharField(max_length=50)
    area = models.FloatField()
    rooms = models.SmallIntegerField()

    description = models.TextField(blank=True)

    class Meta:
        ordering = ["number"]

    def __str__(self) -> str:
        return f"{self.serial} : {self.number}"
