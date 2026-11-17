from django.db import models


class OrganizationScopedModel(models.Model):
    organization = models.ForeignKey(
        "organizations.Organization",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="+",
    )

    class Meta:
        abstract = True

    def clean(self) -> None:
        super().clean()

        if self.pk is not None:
            pass

    def __str__(self) -> str:
        return self.organization.name
