from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from .models import Organization, OrganizationMembership


def create_organization_member(
    *,
    organization: Organization,
    username: str,
    password: str,
    first_name: str = "",
    last_name: str = "",
) -> OrganizationMembership:
    """Provision an active membership using validated account profile fields."""
    user_fields = {
        "username": User.normalize_username(username),
        "first_name": first_name,
        "last_name": last_name,
    }
    try:
        validate_password(password, user=User(**user_fields))
    except ValidationError as exc:
        raise ValidationError({"password": exc.error_list}) from exc

    try:
        with transaction.atomic():
            user = User.objects.create_user(password=password, **user_fields)
            return OrganizationMembership.objects.create(
                organization=organization,
                user=user,
            )
    except IntegrityError as exc:
        # A concurrent request can claim the username after validation.
        if User.objects.filter(username=user_fields["username"]).exists():
            raise ValidationError(
                {
                    "username": ValidationError(
                        _("A user with that username already exists."),
                        code="unique",
                    )
                }
            ) from exc
        raise
