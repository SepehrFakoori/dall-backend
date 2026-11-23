from django.db import models


class TenantQuerySet(models.QuerySet):
    def for_user(self, user):
        """
        Limit tenants to those with active membership for this user.
        """
        if not user.is_authenticated or not user.is_active or user.pk is None:
            return self.none()

        return self.filter(
            memberships__user_id=user.pk,
            memberships__is_active=True,
        )


class TenantScopedQuerySet(models.QuerySet):
    def for_tenant(self, tenant_id):
        """
        Limit records to a tenants instance or primary key.
        """
        return self.filter(tenant_id=tenant_id)
