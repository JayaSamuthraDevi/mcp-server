import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    UPSTREAM_AUTHORIZATION_ENDPOINT = os.getenv("UPSTREAM_AUTHORIZATION_ENDPOINT")
    UPSTREAM_TOKEN_ENDPOINT = os.getenv("UPSTREAM_TOKEN_ENDPOINT")
    UPSTREAM_CLIENT_ID = os.getenv("UPSTREAM_CLIENT_ID")
    UPSTREAM_CLIENT_SECRET = os.getenv("UPSTREAM_CLIENT_SECRET")
    JWKS_URI = os.getenv("JWKS_URI")
    AUDIENCE = os.getenv("AUDIENCE")
    ISSUER = os.getenv("ISSUER")
    MCP_SERVER_BASE_URL = os.getenv("MCP_SERVER_BASE_URL")

    if not UPSTREAM_AUTHORIZATION_ENDPOINT:
        raise RuntimeError("Upstream authorization endpoint missing in environment variables")
    if not MCP_SERVER_BASE_URL:
        raise RuntimeError("MCP server base URL missing in environment variables")
config = Config()
