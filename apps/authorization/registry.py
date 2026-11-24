from django.core.exceptions import ImproperlyConfigured

REGISTRY: dict[str, dict] = {}


def register(codename: str, label: str) -> str:
    if codename in REGISTRY:
        raise ImproperlyConfigured(f"Permission {codename} already registered.")
    REGISTRY[codename] = {"label": label, "module": codename.split(".")[0]}
    return codename
