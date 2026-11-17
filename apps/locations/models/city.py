from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(
        "locations.Province",
        on_delete=models.PROTECT,
        related_name="cities",
    )

    class Meta:
        ordering = ["name", "pk"]

    def __str__(self) -> str:
        return self.name
