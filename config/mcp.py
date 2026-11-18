"""Standalone MCP ASGI entry point; Django's HTTP app runs separately."""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.mcp.http import create_application

application = create_application()
