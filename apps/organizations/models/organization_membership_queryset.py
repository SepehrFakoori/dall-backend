from django.db import models


class OrganizationMembershipQuerySet(models.QuerySet):
    def for_organization(self, organization):
        """Memberships in an organization (instance or primary key)."""
        return self.filter(organization=organization)

    def for_user(self, user):
        """All memberships for a saved user, including inactive memberships."""
        if not user.is_authenticated or user.pk is None:
            return self.none()

        return self.filter(user=user)

    def active(self):
        """Memberships whose is_active flag is true."""
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)
