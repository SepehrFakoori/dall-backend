import asyncio

from django.test import override_settings
from fastmcp import Client
from fastmcp.utilities.asgi_transport import (
    StreamingASGITransport,
    run_asgi_lifespan,
)
from fastmcp.client.transports.http import StreamableHttpTransport
import httpx2

from core.mcp.server import create_server


def test_http_discovery_and_status():
    """Exercise the deployed ASGI application, including its lifespan and route."""
    from config.mcp import application

    async def check():
        async with run_asgi_lifespan(application):

            def client_factory(**kwargs):
                return httpx2.AsyncClient(
                    transport=StreamingASGITransport(app=application), **kwargs
                )

            transport = StreamableHttpTransport(
                "http://testserver/mcp", httpx_client_factory=client_factory
            )
            async with Client(transport) as client:
                tools = await client.list_tools()
                assert [tool.name for tool in tools] == ["system_status"]
                assert tools[0].annotations.read_only_hint is True
                result = await client.call_tool("system_status", {})
                assert result.data == {"service": "dall-mcp", "status": "ok"}

    asyncio.run(check())


def test_registry_controls_exposed_tools():
    """Removing an app from the registry removes its tools from discovery."""

    async def check():
        async with Client(create_server()) as client:
            assert await client.list_tools() == []

    with override_settings(MCP_SERVERS={}):
        asyncio.run(check())
