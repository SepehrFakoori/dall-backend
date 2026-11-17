from core.models import SoftDeleteQuerySet


class OrganizationQuerySet(SoftDeleteQuerySet):
    def for_user(self, user):
        if not user.is_authenticated or user.pk is None:
            return self.none()

        return self.filter(memberships__user=user, memberships__is_active=True)
