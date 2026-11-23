from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError

from apps.users.models import User
from ..models import Tenant, Membership


def create_tenant_member(
    *,
    tenant: Tenant,
    username: str,
    password: str,
    first_name: str,
    last_name: str,
) -> Membership:
    """
    Provision an active membership using validated account profile fields.
    """
    user_fields = {
        "username": User.normalize_username(username),
        "first_name": first_name,
        "last_name": last_name,
    }

    try:
        validate_password(password=password, user=User(**user_fields))
    except ValidationError as exc:
        raise ValidationError({"password": exc.error_list}) from exc

    try:
        with transaction.atomic():
            user = User.objects.create_user(password=password, **user_fields)
            return Membership.objects.create(
                tenant=tenant,
                user=user,
            )
    except IntegrityError as exc:
        # A concurrent request can claim the username after validation.
        if User.objects.filter(username=user_fields["username"]).exists():
            raise ValidationError(
                {
                    "username": ValidationError(
                        "username already exists.",
                        code="unique",
                    )
                }
            ) from exc
        raise
