from fastmcp import FastMCP
import uvicorn
from middleware.Authentication_middleware import AuthMiddleware
from helpers.logging_config import setup_json_logging
from middleware.logging_middleware import LoggingMiddleware
from tools.loader import load_tools

setup_json_logging()

mcp = FastMCP(
    "mcp-service",
    middleware=[
        LoggingMiddleware(),
        AuthMiddleware()
    ]
)

load_tools(mcp)

if __name__ == "__main__":
    print("=" * 70)
    print("Starting MCP Service Server")
    print("=" * 70)
    print("URL: http://0.0.0.0:8000/mcp")
    print("Transport: streamable_http_app")
    print("=" * 70)

    # Create HTTP app (streamable_http_app is deprecated as of 2.3.2)
    app = mcp.http_app()

    # Run with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
