from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20, blank=True)

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="units",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
