from django.db import models


class LocationQuerySet(models.QuerySet):
    def for_organization(self, organization):
        """Locations in an organization (instance or primary key)"""
        return self.filter(organization=organization)

    def for_user(self, user):
        """
        All locations in nondeleted organizations where the user is an active member.
        This scopes by organization membership, not individual location assignment.
        """
        if not user.is_authenticated or user.pk is None:
            return self.none()

        return self.filter(
            organization__is_deleted=False,
            organization__memberships__user=user,
            organization__memberships__is_active=True,
        )
