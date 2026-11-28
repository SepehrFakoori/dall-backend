from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class AccessConfig(AppConfig):
    name = "apps.access"

    def ready(self) -> None:
        # imports <app>.permissions for every installed app.
        autodiscover_modules("permissions")
