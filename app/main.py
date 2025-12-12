from fastmcp import FastMCP
from tools.greetings import hello
from tools.compute_tools import get_compute_offerings
from tools.vpn_tools import get_vpn_user_cost
from helpers.logging_config import configure_logging
from core.keycloak import keycloak_auth

configure_logging()
mcp = FastMCP(name="My Protected Server",   auth = keycloak_auth)

mcp.tool()(hello)
mcp.tool()(get_compute_offerings)
mcp.tool()(get_vpn_user_cost)

mcp_http_app = mcp.http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:mcp_http_app", host="0.0.0.0", port=8000)
