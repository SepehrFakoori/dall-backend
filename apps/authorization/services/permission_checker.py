from ..models import UserRole


def has_permission(user, permission_code):
    if not user.is_authenticated:
        return False

    return UserRole.objects.filter(
        user=user,
        role__permissions__code=permission_code,
    ).exists()
