from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name", "pk"]

    def __str__(self) -> str:
        return self.name
