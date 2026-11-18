from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name", "pk"]

    def __str__(self) -> str:
        return self.name
