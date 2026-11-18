from django.conf import settings
from starlette.applications import Starlette

from .server import create_server


def create_application() -> Starlette:
    """Build a fresh MCP HTTP application from the current Django settings."""
    return create_server().http_app(
        path="/mcp",
        stateless_http=True,
        host_origin_protection=True,
        allowed_hosts=settings.MCP_ALLOWED_HOSTS,
        allowed_origins=settings.MCP_ALLOWED_ORIGINS,
    )
