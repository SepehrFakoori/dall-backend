from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .location_queryset import LocationQuerySet


class Location(models.Model):
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.PROTECT,
        related_name="locations",
    )
    town = models.CharField(max_length=255, blank=True)
    address = models.TextField()
    postal_code = models.PositiveIntegerField()
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(Decimal("-90")),
            MaxValueValidator(Decimal("90")),
        ],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(Decimal("-180")),
            MaxValueValidator(Decimal("180")),
        ],
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
    )

    objects = LocationQuerySet.as_manager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(latitude__isnull=True, longitude__isnull=True)
                | models.Q(latitude__isnull=False, longitude__isnull=False),
                name="location_coordinate_together",
            ),
        ]

    @property
    def province(self):
        return self.city.province

    def __str__(self) -> str:
        return self.address
