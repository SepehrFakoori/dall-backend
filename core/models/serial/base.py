from django.db import models, router, transaction

from .serial_counter import SerialCounter


class ScopedSerialModel(models.Model):
    serial_prefix: str
    serial_scope_field: str

    serial = models.CharField(max_length=50, editable=False)

    class Meta:
        abstract = True

    def save(self, *, using=None, **kwargs):
        if (
            not self._state.adding
            or kwargs.get("force_update")
            or kwargs.get("update_fields") is not None
        ):
            return super().save(using=using, **kwargs)

        scope_field = self._meta.get_field(self.serial_scope_field)
        scope_id = scope_field.target_field.get_prep_value(
            getattr(self, scope_field.attname)
        )
        if scope_id is None:
            raise ValueError(f"Set {self.serial_scope_field} before saving.")

        using = using or router.db_for_write(type(self), instance=self)

        with transaction.atomic(using=using):
            counter, _ = SerialCounter.objects.using(using).update_or_create(
                model_label=self._meta.concrete_model._meta.label_lower,
                scope_id=str(scope_id),
                create_defaults={"last_value": 1},
                defaults={"last_value": models.F("last_value") + 1},
            )
            counter.refresh_from_db(using=using, fields=["last_value"])
            self.serial = f"{self.serial_prefix.upper()}-{counter.last_value:06d}"
            return super().save(using=using, **kwargs)
