from __future__ import annotations
from dataclasses import dataclass
from fastmcp.server.dependencies import get_access_token
import logging

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Credentials:
    api_key: str | None = None
    secret_key: str | None = None
    base_url: str | None = None
    zone_uuid: str | None = None

    @staticmethod
    def load() -> "Credentials":
        token = get_access_token()

        if token is None:
            logger.error("No authentication token found. Please authenticate via Keycloak.")
            raise ValueError("Authentication required. Please login before calling tools.")

        claims = token.claims or {}

        api_key = claims.get("api_key")
        secret_key = claims.get("secret_key")
        base_url = claims.get("base_url")
        zone_uuid = claims.get("zone_uuid")

        if not api_key or not secret_key or not base_url:
            logger.error("Missing required credential fields in token claims: %s", claims)
            raise ValueError("Missing required credential fields. Authenticate correctly.")

        return Credentials(
            api_key=api_key,
            secret_key=secret_key,
            base_url=base_url,
            zone_uuid=zone_uuid,
        )

    def to_headers(self) -> dict[str, str]:
        return {
            "apikey": self.api_key,
            "secretkey": self.secret_key,
        }
