from dataclasses import dataclass

from django.core.exceptions import ImproperlyConfigured


@dataclass(frozen=True)
class PermissionDefinition:
    code: str
    label: str
    app: str
    scoped: bool = True  # False for codes where own/all makes no sense (role.manage)


_registry: dict[str, PermissionDefinition] = {}


def register(
    app: str,
    prefix: str,
    permissions: dict[str, str],
    *,
    unscoped=(),
):
    """
    app: the owning app label (for grouping in the UI)
    prefix: the resource namespace the app owns, e.g. "checks"
    permissions: {"check.view": "View checks", ...}
    """
    for code, label in permissions.items():
        if not code.startswith(f"{prefix}."):
            raise ImproperlyConfigured(f"{code!r} must start with '{prefix}.'")
        if code in _registry:
            raise ImproperlyConfigured(f"Permission {code!r} registered twice")
        _registry[code] = PermissionDefinition(
            code=code,
            label=label,
            app=app,
            scoped=code not in unscoped,
        )


def is_registered(code: str) -> bool:
    return code in _registry


def all_permissions() -> list[PermissionDefinition]:
    return sorted(_registry.values(), key=lambda p: (p.app, p.code))


def get_permission(code: str) -> PermissionDefinition | None:
    return _registry.get(code)
