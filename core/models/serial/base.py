from django.db import models


class SerialModel(models.Model):
    serial_prefix: str | None = None

    serial = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.serial and self.serial_prefix:
            super().save(*args, **kwargs)
            self.serial = f"{self.serial_prefix.upper()}-{self.pk:06d}"
            super().save(update_fields=["serial"])
            return
        super().save(*args, **kwargs)
