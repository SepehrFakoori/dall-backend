from django.db import models

from apps.projects.models import ProjectScopedModel


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name="cities",
    )

    class Meta:
        ordering = ["-name"]
        constraints = [
            models.UniqueConstraint(
                fields=["province", "name"],
                name="unique_province_city",
            )
        ]

    def __str__(self) -> str:
        return self.name


class Location(ProjectScopedModel):
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
    )
    town = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    postal_code = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField()
    longitude = models.DecimalField()

    def __str__(self) -> str:
        return f"{self.city} @ {self.province}"
