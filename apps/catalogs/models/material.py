from django.db import models

from core.models import SerialModel


class Material(SerialModel):
    serial_prefix = "MAT"

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
