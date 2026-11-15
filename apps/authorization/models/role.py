from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    permissions = models.ManyToManyField(
        "authorization.Permission",
        blank=True,
        related_name="roles",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self) -> str:
        return self.name
