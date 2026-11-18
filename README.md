# dall-backend

## MCP

FastMCP provides a separate Streamable HTTP endpoint for ChatGPT. Each app owns
its tools; `core/mcp/server.py` composes the factories explicitly registered in
`MCP_SERVERS` in Django settings. For example, the `system` server's `status` tool
is exposed as `system_status`.

Run from the project root with the project's virtual environment activated:

```powershell
python -m uvicorn config.mcp:application --host 127.0.0.1 --port 8001 --reload
```

The MCP URL is `http://127.0.0.1:8001/mcp`. Django's existing REST server runs
separately on port 8000. Uvicorn manages the MCP application's startup and
shutdown lifespan. Stateless HTTP avoids server-side session affinity; it does
not provide durable conversational state.

`config/mcp.py` initializes Django, then calls `create_application()` in
`core/mcp/http.py`. That factory builds a fresh server and applies the HTTP
configuration. Tests use the same factory with their own registry, so adding
app tools does not change the test setup.

The current endpoint has no authentication and exposes only `system_status`,
which returns a fixed service status without reading the database. DRF's JWT,
permission, and throttle settings do not apply to this separate endpoint.

Host/Origin validation is enabled through FastMCP's built-in request guard.
It accepts loopback/bound hosts and same-origin requests by default. Configure
additional trusted hosts and browser origins through these environment variables
before starting the server:

```powershell
$env:MCP_ALLOWED_HOSTS = "your-tunnel.example.com"
# Only needed for a browser client running on a different origin:
$env:MCP_ALLOWED_ORIGINS = "https://your-client.example.com"
```

Values are comma-separated. Hosts contain no scheme or path; origins include
the scheme and any non-default port. Add the actual tunnel hostname to
`MCP_ALLOWED_HOSTS` when using a tunnel. Requests without an Origin header can
connect when their Host is allowed, as is typical for server-to-server clients.
These checks validate request headers; they do not identify users, grant access
to private data, or configure CORS response headers.

### Connecting ChatGPT

ChatGPT requires a reachable endpoint. Publish this diagnostic endpoint through
an HTTPS development tunnel, or use OpenAI's supported Secure MCP Tunnel.
In ChatGPT's custom MCP app setup, use the reachable `/mcp` URL and select
**No authentication**. Ask ChatGPT to check the Dall service status.
Localhost alone is not reachable by a remote ChatGPT connection. Availability
of custom MCP apps depends on the account and workspace configuration.

See [OpenAI's connection guide](https://help.openai.com/en/articles/12584461).
This repository does not configure a tunnel or publish a server.

### Adding an app

Create `apps/<app>/mcp.py` with a `create_server()` factory returning a `FastMCP`
instance. Register its dotted factory path under a unique namespace:

```python
MCP_SERVERS = {
    "system": "core.mcp.system.create_server",
    # After implementing the factory:
    # "projects": "apps.projects.mcp.create_server",
}
```

Use the factory in `core/mcp/system.py` as a working example. Factories should
register tools without querying the database during startup. Registration is
explicit so new app modules are not automatically published.

The registry must be a mapping with non-empty string namespaces. Each value must
be an importable dotted path to a callable that takes no arguments and returns a
`FastMCP` instance. Invalid namespaces, unresolved paths, non-callable targets,
and incorrect return types raise Django's `ImproperlyConfigured` with the
offending entry. Exceptions inside a factory keep their original traceback.

Keep business operations in app services, reusable by REST views and MCP tools.
Use typed inputs and JSON-serializable outputs, bounded list results, and accurate
tool descriptions and annotations. For synchronous ORM operations, use a sync
tool function (FastMCP runs it in a worker thread by default), or use Django's
async ORM APIs in async tools.

Before registering tools that access private records or perform writes, implement
MCP authentication, resolve the caller, and enforce permissions and organization
access in shared services. Tool annotations describe behavior to the client;
they do not enforce authorization.

### Verification

```powershell
python -m pytest core/mcp/test_server.py -q
```
