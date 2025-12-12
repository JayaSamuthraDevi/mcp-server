from services.token_service import current_claims

def hello() -> str:
    claims = current_claims()
    return f"Hello {claims.name}! Email: {claims.email}"
