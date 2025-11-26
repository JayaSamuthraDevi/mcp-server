from fastmcp import FastMCP
from helpers.logging_config import setup_json_logging
from middleware.logging_middleware import LoggingMiddleware
from tools.loader import load_tools

setup_json_logging()

mcp = FastMCP(
    "mcp-service",
    middleware=[
        LoggingMiddleware()
    ]
)

load_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000)
