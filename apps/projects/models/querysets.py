from django.db import models


class ProjectScopedQuerySet(models.QuerySet):
    def for_project(self, project_id):
        """
        Limit records to a project instance or primary key.
        """
        return self.filter(project_id=project_id)
