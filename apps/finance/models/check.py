from django.db import models


class Check(models.Model):
    purpose = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return ""
