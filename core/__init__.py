from fastmcp.server.auth.oauth_proxy import OAuthProxy
from fastmcp.server.auth.providers.jwt import JWTVerifier
from core.config import config

# Initialize OAuth Proxy
keycloak_auth = OAuthProxy(
    upstream_authorization_endpoint=config.UPSTREAM_AUTHORIZATION_ENDPOINT,
    upstream_token_endpoint=config.UPSTREAM_TOKEN_ENDPOINT,
    upstream_client_id=config.UPSTREAM_CLIENT_ID,
    upstream_client_secret=config.UPSTREAM_CLIENT_SECRET,
    token_verifier=JWTVerifier(
        jwks_uri=config.JWKS_URI,
        issuer=config.ISSUER,
        audience=config.AUDIENCE,
        required_scopes=[],
    ),
    base_url=config.MCP_SERVER_BASE_URL,
)