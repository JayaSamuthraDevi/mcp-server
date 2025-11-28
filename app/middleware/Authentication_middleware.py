"""Authentication middleware for FastMCP requests.

This middleware extracts credentials from incoming request headers and makes
them available to tools via Context state.
"""

from __future__ import annotations

from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import Middleware, MiddlewareContext

from core.constants import (
    MCP_EXEMPT_METHODS,
    STATE_KEY_API_KEY,
    STATE_KEY_BASE_URL,
    STATE_KEY_SECRET_KEY,
    STATE_KEY_ZONE_UUID,
)


class AuthMiddleware(Middleware):
    """Authentication middleware following FastMCP best practices.

    Extracts credentials from incoming request headers and makes them
    available to tools via Context state. No validation - just passes
    through the credentials sent by the LLM client.

    The LLM client reads mcp.json to know what headers to send.
    """

    # Methods that don't require authentication (MCP protocol methods)
    EXEMPT_METHODS = MCP_EXEMPT_METHODS

    async def on_request(self, context: MiddlewareContext, call_next):
        print("\n" + "=" * 60)
        print("[AUTH] Request received")
        print("=" * 60)
        print(f"[AUTH] Method: {context.method}")

        # Skip authentication for MCP protocol methods
        if context.method in self.EXEMPT_METHODS:
            print(f"[AUTH] ⊘ SKIPPED: '{context.method}' is exempt from authentication")
            print("=" * 60 + "\n")
            return await call_next(context)

        # Access HTTP headers from the LLM client request
        try:
            headers = get_http_headers()
            if headers is None:
                headers = {}
                print("[AUTH] WARNING: get_http_headers() returned None")
        except Exception as e:
            print(f"[AUTH] ERROR: Failed to get headers: {e}")
            headers = {}

        print(f"[AUTH] Headers received from LLM client: {list(headers.keys())}")

        # Extract credentials from request headers (case-insensitive)
        api_key = headers.get("apikey") or headers.get("Apikey") or headers.get("APIKEY")
        secret_key = headers.get("secretkey") or headers.get("Secretkey") or headers.get("SECRETKEY")
        base_url = headers.get("base_url") or headers.get("Base_url") or headers.get("BASE_URL")
        zone_uuid = headers.get("zone_uuid") or headers.get("Zone_uuid") or headers.get("ZONE_UUID")

        print(f"[AUTH] Received API Key: {api_key[:10]}..." if api_key else "[AUTH] Received API Key: None")
        print(f"[AUTH] Received Secret Key: {secret_key[:10]}..." if secret_key else "[AUTH] Received Secret Key: None")
        print(f"[AUTH] Received Base URL: {base_url}")
        print(f"[AUTH] Received Zone UUID: {zone_uuid}")

        # Require that credentials are present (basic validation)
        if not api_key:
            print("[AUTH] ✗ FAILED: Missing apikey header from LLM client")
            print("=" * 60 + "\n")
            raise ValueError("Missing apikey header. The LLM client must send headers from mcp.json")

        if not secret_key:
            print("[AUTH] ✗ FAILED: Missing secretkey header from LLM client")
            print("=" * 60 + "\n")
            raise ValueError("Missing secretkey header. The LLM client must send headers from mcp.json")

        # Store credentials from request in context state for tools to use
        # Tools will use these credentials when making API calls
        ctx = context.fastmcp_context
        ctx.set_state(STATE_KEY_API_KEY, api_key)
        ctx.set_state(STATE_KEY_SECRET_KEY, secret_key)
        ctx.set_state(STATE_KEY_BASE_URL, base_url)
        ctx.set_state(STATE_KEY_ZONE_UUID, zone_uuid)

        print("[AUTH] ✓ SUCCESS: Credentials extracted from request")
        print("[AUTH] Credentials stored in context state for tools")
        print("=" * 60 + "\n")

        return await call_next(context)


__all__ = ["AuthMiddleware"]
