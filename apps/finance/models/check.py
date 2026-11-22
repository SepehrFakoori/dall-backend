from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.organizations.models import OrganizationScopedModel


class CheckDirection(models.TextChoices):
    RECEIVED = "received"
    ISSUED = "issued"


class CheckType(OrganizationScopedModel):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=10, choices=CheckDirection.choices)

    def __str__(self) -> str:
        return f"{self.name} @ {self.type}"


class CheckStatus(OrganizationScopedModel):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=10, choices=CheckDirection.choices)

    def __str__(self) -> str:
        return f"{self.name} @ {self.type}"


class Check(OrganizationScopedModel):
    purpose = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sayad_id = models.CharField(max_length=100)
    type = models.ForeignKey(
        CheckType,
        on_delete=models.PROTECT,
        related_name="checks",
    )
    status = models.ForeignKey(
        CheckStatus,
        on_delete=models.PROTECT,
        related_name="checks",
    )
    due_date = models.DateField()
    amount = models.PositiveBigIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10**18 - 1),
        ],
    )
    drawer = models.CharField(max_length=255, blank=True, null=True)
    payee = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.purpose
