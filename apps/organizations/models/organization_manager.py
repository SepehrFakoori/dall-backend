from django.db import models

from .organization_queryset import OrganizationQuerySet


class OrganizationManager(models.Manager.from_queryset(OrganizationQuerySet)):
    def get_queryset(self):
        return super().get_queryset().alive()
