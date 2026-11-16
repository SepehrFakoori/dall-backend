from django.db import models

from core.models import SoftDeleteModel


class Organization(SoftDeleteModel):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
