from pydantic import BaseModel

class TokenClaims(BaseModel):
    email: str | None = None
    name: str | None = None
    base_url: str | None = None
    zone_uuid: str | None = None
    api_key: str | None = None
    secret_key: str | None = None
