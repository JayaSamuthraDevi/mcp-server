from fastmcp.server.dependencies import get_access_token
from models.token_data import TokenClaims

def current_claims() -> TokenClaims:
    token = get_access_token()
    return TokenClaims(**token.claims)
