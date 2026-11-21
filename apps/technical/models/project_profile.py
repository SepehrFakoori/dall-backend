from django.db import models

from apps.projects.models import ProjectScopedModel, Use


class ProjectProfile(ProjectScopedModel):
    uses = models.ManyToManyField("projects.Use", related_name="projects")
    description = models.TextField(blank=True)
