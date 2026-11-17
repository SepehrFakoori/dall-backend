"""Standalone MCP ASGI entry point; Django's HTTP app runs separately."""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.mcp.server import create_server

server = create_server()
application = server.http_app(path="/mcp", stateless_http=True)
