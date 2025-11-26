import json
from pathlib import Path
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_headers

# Global variables to store credentials
EXPECTED_API_KEY = None
EXPECTED_SECRET_KEY = None
BASE_URL = None
ZONE_UUID = None

def load_credentials_from_mcp_json():
    """Load credentials from mcp.json file"""
    global EXPECTED_API_KEY, EXPECTED_SECRET_KEY, BASE_URL, ZONE_UUID

    # Try to find mcp.json in parent directory
    current_dir = Path(__file__).resolve().parent
    mcp_json_path = current_dir.parent.parent / "mcp.json"

    if not mcp_json_path.exists():
        print(f"[WARNING] mcp.json not found at {mcp_json_path}")
        return False

    try:
        with open(mcp_json_path, 'r') as f:
            config = json.load(f)

        # Extract headers from mcp-service configuration
        headers = config.get("mcpServers", {}).get("mcp-service", {}).get("headers", {})

        EXPECTED_API_KEY = headers.get("apikey")
        EXPECTED_SECRET_KEY = headers.get("secretkey")
        BASE_URL = headers.get("base_url")
        ZONE_UUID = headers.get("zone_uuid")

        print("=" * 70)
        print("[CONFIG] Loaded credentials from mcp.json")
        print("=" * 70)
        print(f"[CONFIG] API Key: {EXPECTED_API_KEY[:10]}..." if EXPECTED_API_KEY else "[CONFIG] API Key: Not set")
        print(f"[CONFIG] Secret Key: {EXPECTED_SECRET_KEY[:10]}..." if EXPECTED_SECRET_KEY else "[CONFIG] Secret Key: Not set")
        print(f"[CONFIG] Base URL: {BASE_URL}")
        print(f"[CONFIG] Zone UUID: {ZONE_UUID}")
        print("=" * 70)

        return True

    except Exception as e:
        print(f"[ERROR] Failed to load mcp.json: {e}")
        return False

# Load credentials on module import
load_credentials_from_mcp_json()

class AuthMiddleware(Middleware):
    """
    Authentication middleware following FastMCP best practices.

    Uses get_http_headers() to access request headers and set_state()
    to pass authenticated credentials to tools via Context.
    """

    # Methods that don't require authentication (MCP protocol methods)
    EXEMPT_METHODS = {
        "initialize",
        "initialized",
        "ping",
        "notifications/cancelled",
        "tools/list",
        "resources/list",
        "prompts/list",
        "completion/complete"
    }

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

        # Access HTTP headers using FastMCP's recommended approach
        try:
            headers = get_http_headers()
            if headers is None:
                headers = {}
                print("[AUTH] WARNING: get_http_headers() returned None")
        except Exception as e:
            print(f"[AUTH] ERROR: Failed to get headers: {e}")
            headers = {}

        print(f"[AUTH] Headers received: {headers}")
        print(f"[AUTH] Header keys: {list(headers.keys())}")

        # Extract credentials from headers (case-insensitive)
        api_key = headers.get("apikey") or headers.get("Apikey") or headers.get("APIKEY")
        secret_key = headers.get("secretkey") or headers.get("Secretkey") or headers.get("SECRETKEY")
        base_url = headers.get("base_url") or headers.get("Base_url") or headers.get("BASE_URL")
        zone_uuid = headers.get("zone_uuid") or headers.get("Zone_uuid") or headers.get("ZONE_UUID")

        print(f"[AUTH] Received API Key: {api_key[:10]}..." if api_key else "[AUTH] Received API Key: None")
        print(f"[AUTH] Received Secret Key: {secret_key[:10]}..." if secret_key else "[AUTH] Received Secret Key: None")
        print(f"[AUTH] Received Base URL: {base_url}")
        print(f"[AUTH] Received Zone UUID: {zone_uuid}")

        # Validate API key
        if not api_key:
            print("[AUTH] ✗ FAILED: Missing apikey header")
            print("=" * 60 + "\n")
            raise ValueError("Missing apikey header. Required headers: apikey, secretkey, base_url, zone_uuid")

        if api_key != EXPECTED_API_KEY:
            print("[AUTH] ✗ FAILED: Invalid API key")
            print("=" * 60 + "\n")
            raise ValueError("Invalid API key")

        # Validate secret key
        if not secret_key:
            print("[AUTH] ✗ FAILED: Missing secretkey header")
            print("=" * 60 + "\n")
            raise ValueError("Missing secretkey header. Required headers: apikey, secretkey, base_url, zone_uuid")

        if secret_key != EXPECTED_SECRET_KEY:
            print("[AUTH] ✗ FAILED: Invalid secret key")
            print("=" * 60 + "\n")
            raise ValueError("Invalid secret key")

        # Store credentials in context state for use in tools
        # Using set_state() is the FastMCP recommended approach
        ctx = context.fastmcp_context
        ctx.set_state("api_key", api_key)
        ctx.set_state("secret_key", secret_key)
        ctx.set_state("base_url", base_url or BASE_URL)
        ctx.set_state("zone_uuid", zone_uuid or ZONE_UUID)

        print("[AUTH] ✓ SUCCESS: Authentication passed")
        print("[AUTH] Credentials stored in context state")
        print("=" * 60 + "\n")

        return await call_next(context)
