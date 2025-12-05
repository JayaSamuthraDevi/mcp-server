import logging
from fastmcp import FastMCP, Context
from fastmcp.server.auth.oauth_proxy import OAuthProxy
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.dependencies import get_access_token

logging.basicConfig(level=logging.INFO)

# Initialize OAuth Proxy
auth = OAuthProxy(
    upstream_authorization_endpoint="http://localhost:8080/realms/myrealm/protocol/openid-connect/auth",
    upstream_token_endpoint="http://localhost:8080/realms/myrealm/protocol/openid-connect/token",
    upstream_client_id="mcp-server-client",
    upstream_client_secret="redacted",
    token_verifier=JWTVerifier(
        jwks_uri="http://localhost:8080/realms/myrealm/protocol/openid-connect/certs",
        issuer="http://localhost:8080/realms/myrealm",
        audience="account",
        required_scopes=[],
    ),
    base_url="http://localhost:8000",
)

mcp = FastMCP(name="My Protected Server", auth=auth)

@mcp.tool()
def hello(context: Context) -> str:
    """Greet the authenticated user - similar to Gmail's approach"""
    token = get_access_token()  # returns TokenData
    claims = token.claims       # decoded JWT payload
    print(token)
    user_email = claims.get("email")
    user_name = claims.get("name")

    return f"Hello {user_name}! Email: {user_email}"

mcp_http_app = mcp.http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:mcp_http_app", host="0.0.0.0", port=8000)
