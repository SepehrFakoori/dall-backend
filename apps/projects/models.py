from django.db import models

from core.models import SerialModel
from apps.organizations.models import OrganizationScopedModel


class Project(OrganizationScopedModel, SerialModel):
    serial_prefix = "PRJ"

    title = models.CharField(max_length=100, verbose_name="Project title")
    name = models.CharField(max_length=100, verbose_name="Internal name", blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.serial} @ {self.name}"
