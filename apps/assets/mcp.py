from fastmcp import FastMCP

from .models import Asset


def create_server() -> FastMCP:
    server = FastMCP("Assets", mask_error_details=True)

    @server.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    def list_assets() -> dict:
        """
        List non-deleted assets, newest first.
        """
        queryset = Asset.objects.all()

        assets = list(queryset.values("id", "serial", "name", "description"))

        return {"result": assets}

    return server
