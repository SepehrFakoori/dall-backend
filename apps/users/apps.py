from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

    def ready(self) -> None:
        from apps.files.policies import register
        from .upload_policies import UPLOAD_POLICIES

        for policy in UPLOAD_POLICIES:
            register(policy)
