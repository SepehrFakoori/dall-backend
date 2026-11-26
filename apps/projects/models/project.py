from django.db import models

from core.models import ScopedSerialModel


class Project(ScopedSerialModel):
    serial_prefix = "PRJ"
    serial_scope_field = "tenant"

    title = models.CharField(max_length=100, verbose_name="Project title")
    name = models.CharField(max_length=100, verbose_name="Internal name", blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.serial} @ {self.name}"
