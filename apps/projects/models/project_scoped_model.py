from django.db import models

from .querysets import ProjectScopedQuerySet


class ProjectScopedModel(models.Model):
    """
    Base model for projects scoped model
    """

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="+",
    )

    objects = ProjectScopedQuerySet.as_manager()

    class Meta:
        abstract = True
