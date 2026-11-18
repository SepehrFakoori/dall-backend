from collections.abc import Mapping

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from fastmcp import FastMCP


def create_server() -> FastMCP:
    """Compose explicitly registered app servers under unique namespaces."""
    registry = settings.MCP_SERVERS
    if not isinstance(registry, Mapping):
        raise ImproperlyConfigured(
            "MCP_SERVERS must map namespaces to dotted server factory paths."
        )

    server = FastMCP(
        "Dall",
        instructions="Tools provided by the Dall application.",
        mask_error_details=True,
    )
    for namespace, factory_path in registry.items():
        if not isinstance(namespace, str) or not namespace.strip():
            raise ImproperlyConfigured(
                f"MCP_SERVERS namespace {namespace!r} must be a non-empty string."
            )
        entry = f"MCP_SERVERS[{namespace!r}]"
        if not isinstance(factory_path, str) or not factory_path.strip():
            raise ImproperlyConfigured(f"{entry} must be a dotted server factory path.")
        try:
            factory = import_string(factory_path)
        except ImportError as exc:
            raise ImproperlyConfigured(
                f"{entry}: cannot import {factory_path!r}."
            ) from exc
        if not callable(factory):
            raise ImproperlyConfigured(f"{entry}: {factory_path!r} must be callable.")
        child_server = factory()
        if not isinstance(child_server, FastMCP):
            raise ImproperlyConfigured(
                f"{entry}: {factory_path!r} must return a FastMCP instance."
            )
        server.mount(child_server, namespace=namespace)
    return server
