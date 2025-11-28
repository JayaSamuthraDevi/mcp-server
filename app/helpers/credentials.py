"""Centralized credentials management service.

This module provides a singleton-like service for managing API credentials
extracted from the FastMCP context, eliminating prop drilling throughout the application.
"""

from __future__ import annotations

from dataclasses import dataclass

from fastmcp import Context


@dataclass(frozen=True)
class Credentials:
    """Immutable credentials data container."""

    api_key: str
    secret_key: str
    base_url: str
    zone_uuid: str | None = None

    def to_headers(self) -> dict[str, str]:
        """Convert credentials to HTTP headers format."""
        return {
            "apikey": self.api_key,
            "secretkey": self.secret_key,
        }


class CredentialsService:
    """Service for extracting and managing credentials from FastMCP context."""

    @staticmethod
    def from_context(context: Context) -> Credentials:
        """Extract credentials from FastMCP context state.

        Args:
            context: FastMCP context containing state set by AuthMiddleware

        Returns:
            Credentials: Immutable credentials object

        Raises:
            ValueError: If required credentials are missing from context
        """
        api_key = context.get_state("api_key")
        secret_key = context.get_state("secret_key")
        base_url = context.get_state("base_url")
        zone_uuid = context.get_state("zone_uuid")

        if not api_key:
            raise ValueError("API key not found in context")
        if not secret_key:
            raise ValueError("Secret key not found in context")
        if not base_url:
            raise ValueError("Base URL not found in context")

        return Credentials(
            api_key=api_key,
            secret_key=secret_key,
            base_url=base_url,
            zone_uuid=zone_uuid,
        )


# Export commonly used items
__all__ = ["Credentials", "CredentialsService"]
