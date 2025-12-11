from fastmcp import FastMCP
import uvicorn
from tools.loader import load_tools
from core.keycloak import keycloak_auth

mcp = FastMCP(
    "mcp-service",
    auth = keycloak_auth
)

load_tools(mcp)

if __name__ == "__main__":
    # Create HTTP app (streamable_http_app is deprecated as of 2.3.2)
    app = mcp.http_app()

    # Run with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
