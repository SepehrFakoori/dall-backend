from django.db import models

from core.models import SoftDeleteModel, SerialModel


class Asset(SoftDeleteModel, SerialModel):
    serial_prefix = "AST"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name
