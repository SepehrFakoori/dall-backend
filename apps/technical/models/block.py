from django.db import models

from core.models import ScopedSerialModel
from apps.projects.models import ProjectScopedModel


class Block(ScopedSerialModel, ProjectScopedModel):
    serial_prefix = "BLC"
    serial_scope_field = "project"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name
