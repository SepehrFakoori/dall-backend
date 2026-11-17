from fastmcp import FastMCP


def create_server() -> FastMCP:
    """Build public diagnostic tools without accessing application data."""
    server = FastMCP("System", mask_error_details=True)

    @server.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    def status() -> dict[str, str]:
        """Check that the Dall MCP service responds; does not check dependencies."""
        return {"service": "dall-mcp", "status": "ok"}

    return server
