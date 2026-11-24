from django.db import models


class ActiveModel(models.Model):
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def activate(self) -> None:
        if self.is_active:
            return

        self.is_active = True
        self.save(update_fields=["is_active"])

    def deactivate(self) -> None:
        if not self.is_active:
            return

        self.is_active = False
        self.save(update_fields=["is_active"])
