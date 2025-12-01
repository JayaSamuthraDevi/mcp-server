import os
from dataclasses import dataclass
from fastmcp import Context
from mcp_server_stdio.exceptions.custom_exceptions import MissingCredentialsError

@dataclass
class Credentials:
    api_key: str
    secret_key: str
    base_url: str
    zone_uuid: str

    def validate(self):
        """Validate the credential values and raise clear errors."""
        missing = []
    
        if not self.api_key:
            missing.append("API_KEY")
        if not self.secret_key:
            missing.append("SECRET_KEY")
        if not self.base_url:
            missing.append("BASE_URL")

        if missing:
            raise MissingCredentialsError(
                f"Missing required credentials: {', '.join(missing)}. "
                f"Please set them as environment variables."
            )

    def to_headers(self) -> dict[str, str]:
        self.validate()
        return {
            "apikey": self.api_key,
            "secretkey": self.secret_key,
        }

class CredentialsService:

    @staticmethod
    def from_env() -> Credentials:
        creds = Credentials(
            api_key=os.getenv("API_KEY", ""),
            secret_key=os.getenv("SECRET_KEY", ""),
            base_url=os.getenv("BASE_URL", ""),
            zone_uuid=os.getenv("ZONE_UUID", "")
        )
        creds.validate()
        return creds

    @staticmethod
    def from_context(context: Context) -> Credentials:
        creds = getattr(context, "credentials", CredentialsService.from_env())
        creds.validate()
        return creds
