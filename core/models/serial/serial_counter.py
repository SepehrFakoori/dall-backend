from django.db import models, transaction


class SerialCounter(models.Model):
    model_label = models.CharField(max_length=255)
    scope_id = models.CharField(
        max_length=64, blank=True, default=""
    )  # "" = whole company
    last_value = models.PositiveBigIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["model_label", "scope_id"],
                name="unique_serial_counter_scope",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.model_label}[{self.scope_id or 'company'}]: {self.last_value}"

    @classmethod
    def next_value(cls, model_label: str, scope_id: str = "", *, using: str) -> int:
        """Return the next number. Must run inside transaction.atomic."""
        if not transaction.get_connection(using).in_atomic_block:
            raise RuntimeError(
                "SerialCounter.next_value must run inside transaction.atomic()."
            )
        counter, _ = (
            cls.objects.using(using)
            .select_for_update()  # row lock held until the transaction ends
            .get_or_create(model_label=model_label, scope_id=scope_id)
        )
        counter.last_value += 1
        counter.save(update_fields=["last_value"])
        return counter.last_value
