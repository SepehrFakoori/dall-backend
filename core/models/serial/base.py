from django.db import models, router, transaction

from .serial_counter import SerialCounter


class ScopedSerialModel(models.Model):
    serial_prefix: str
    serial_scope_field: str | None = None  # None = number per company

    serial = models.CharField(max_length=50, editable=False)

    class Meta:
        abstract = True

    def _serial_scope_id(self) -> str:
        if self.serial_scope_field is None:
            return ""
        field = self._meta.get_field(self.serial_scope_field)
        value = field.target_field.get_prep_value(getattr(self, field.attname))
        if value is None:
            raise ValueError(f"Set {self.serial_scope_field} before saving.")
        return str(value)

    def save(self, *args, **kwargs):
        # Only new rows without a serial get one (also skips fixtures and imports)
        if (
            not self._state.adding
            or self.serial
            or kwargs.get("force_update")
            or kwargs.get("update_fields") is not None
        ):
            return super().save(*args, **kwargs)

        using = kwargs.get("using") or router.db_for_write(type(self), instance=self)
        kwargs["using"] = using
        scope_id = self._serial_scope_id()

        with transaction.atomic(using=using):
            value = SerialCounter.next_value(
                self._meta.concrete_model._meta.label_lower,
                scope_id,
                using=using,
            )
            self.serial = f"{self.serial_prefix.upper()}-{value:06d}"
            return super().save(*args, **kwargs)
