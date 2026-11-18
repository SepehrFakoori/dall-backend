from django.db import models


class OrganizationQuerySet(models.QuerySet):
    def for_user(self, user):
        """
        Limit organization to those with active membership for this user.
        """
        if not user.is_authenticated or not user.is_active or user.pk is None:
            return self.none()

        return self.filter(
            memberships__user_id=user.pk,
            memberships__is_active=True,
        )


class OrganizationScopedQuerySet(models.QuerySet):
    def for_organization(self, organization_id):
        """
        Limit records to an organizations instance or primary key.
        """
        return self.filter(organization_id=organization_id)


class DepartmentQuerySet(models.QuerySet):
    def for_user(self, user):
        """
        Limit department membership for this user.
        """
        if not user.is_authenticated or not user.is_active or user.pk is None:
            return self.none()

        return self.filter(
            memberships__user_id=user.pk,
            memberships__is_active=True,
        )
