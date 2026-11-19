from django.db import models


class SerialCounter(models.Model):
    model_label = models.CharField(max_length=255)
    scope_id = models.CharField(max_length=64)
    last_value = models.PositiveBigIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["model_label", "scope_id"],
                name="unique_serial_counter_scope",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.scope_id} @ {self.model_label}: {self.last_value}"
