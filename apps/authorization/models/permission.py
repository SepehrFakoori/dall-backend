from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.code
