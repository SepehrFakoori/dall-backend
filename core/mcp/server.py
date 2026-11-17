from django.conf import settings
from django.utils.module_loading import import_string
from fastmcp import FastMCP


def create_server() -> FastMCP:
    """Compose explicitly registered app servers under unique namespaces."""
    server = FastMCP(
        "Dall",
        instructions="Tools provided by the Dall application.",
        mask_error_details=True,
    )
    for namespace, factory_path in settings.MCP_SERVERS.items():
        factory = import_string(factory_path)
        server.mount(factory(), namespace=namespace)
    return server
