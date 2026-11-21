from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.projects.models import ProjectScopedModel

LATITUDE_LIMIT = 90
LONGITUDE_LIMIT = 180


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)

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
        null=True,
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
    )
    town = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    postal_code = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(-LATITUDE_LIMIT),
            MaxValueValidator(LATITUDE_LIMIT),
        ],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(-LONGITUDE_LIMIT),
            MaxValueValidator(LONGITUDE_LIMIT),
        ],
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(latitude__isnull=True, longitude__isnull=True)
                    | models.Q(
                        latitude__isnull=False,
                        longitude__isnull=False,
                        latitude__range=(-LATITUDE_LIMIT, LATITUDE_LIMIT),
                        longitude__range=(-LONGITUDE_LIMIT, LONGITUDE_LIMIT),
                    )
                ),
                name="location_valid_coordinate_pair",
            ),
        ]

    def __str__(self) -> str:
        return self.address
