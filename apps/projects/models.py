from django.db import models

from core.models import SoftDeleteModel, SerialModel


class Project(SoftDeleteModel, SerialModel):
    serial_prefix = "PRJ"

    title = models.CharField(max_length=255)
    internal_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    asset = models.ForeignKey(
        "assets.Asset",
        on_delete=models.CASCADE,
        related_name="projects",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
