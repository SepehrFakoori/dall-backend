"""Standalone MCP ASGI entry point; Django's HTTP app runs separately."""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.mcp.server import create_server

mcp = create_server()
application = mcp.http_app(path="/mcp", stateless_http=True)
