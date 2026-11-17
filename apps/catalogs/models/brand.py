from django.db import models

from core.models import SerialModel


class Brand(SerialModel):
    serial_prefix = "BRAND"

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
