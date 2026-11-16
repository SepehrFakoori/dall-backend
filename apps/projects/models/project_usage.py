from django.db import models


class ProjectUsage(models.Model):
    name = models.CharField(max_length=100)
    code = models.SlugField(max_length=100)

    def __str__(self) -> str:
        return self.name
