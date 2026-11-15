from typing import Any

from django.db import models

from .managers import SoftDeleteManager, AllObjectsManager


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def delete(self, using: Any | None = None, keep_parents: bool = False):
        self.is_deleted = True
        self.save(using=using, update_fields=["is_deleted"])

    def hard_delete(self, using: Any | None = None, keep_parents: bool = False):
        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.is_deleted = False
        self.save(update_fields=["is_deleted"])
