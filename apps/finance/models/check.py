from django.db import models


class _Type(models.TextChoices):
    RECEIVED = "received"
    ISSUED = "issued"


class CheckType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=10, choices=_Type.choices)

    def __str__(self) -> str:
        return f"{self.name} @ {self.type}"


class CheckStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=10, choices=_Type.choices)

    def __str__(self) -> str:
        return self.name


class Check(models.Model):
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
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    drawer = models.CharField(max_length=255, blank=True, null=True)
    payee = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.purpose
