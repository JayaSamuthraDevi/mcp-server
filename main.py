import logging
from fastmcp import FastMCP, Context
from fastmcp.server.auth.oauth_proxy import OAuthProxy
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.dependencies import get_access_token
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.DEBUG)

# Initialize OAuth Proxy
auth = OAuthProxy(
    upstream_authorization_endpoint="https://keycloak.elasticspace.io:8443/realms/myrealm/protocol/openid-connect/auth",
    upstream_token_endpoint="https://keycloak.elasticspace.io:8443/realms/myrealm/protocol/openid-connect/token",
    upstream_client_id="mcp-server-client",
    upstream_client_secret="nTnSfGoO0Z8WnH32Gxw1nsUpzGnPYCtn",
    token_verifier=JWTVerifier(
        jwks_uri="https://keycloak.elasticspace.io:8443/realms/myrealm/protocol/openid-connect/certs",
        issuer="https://keycloak.elasticspace.io:8443/realms/myrealm",
        audience="account",
        required_scopes=[],
    ),
    base_url="https://charming-lime-spoonbill.fastmcp.app",
)

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=[ "http://localhost:6274",
            "https://charming-lime-spoonbill.fastmcp.app"],  # Allow all origins; use specific origins for security
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],  # allow all headers
        expose_headers=["*"]
    )
]

mcp = FastMCP(name="My Protected Server", auth=auth, middleware=middleware)

@mcp.tool()
def hello(context: Context) -> str:
    """Greet the authenticated user - similar to Gmail's approach"""
    token = get_access_token()  # returns TokenData
    claims = token.claims       # decoded JWT payload
    logging.info(f"User claims: {claims}")
    logging.info(f"Token: {token}")
    user_email = claims.get("email")
    user_name = claims.get("name")

    return f"Hello {user_name}! Email: {user_email}, Token: {token}"

mcp_http_app = mcp.http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:mcp_http_app", host="0.0.0.0", port=8080)
