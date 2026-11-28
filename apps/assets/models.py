from django.db import models


class Asset(models.Model):
    # Serial per company
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name
