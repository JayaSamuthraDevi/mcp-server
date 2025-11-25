from fastmcp import FastMCP
from middleware.logging_middleware import LoggingMiddleware
from tools.loader import load_tools

mcp = FastMCP(
    "mcp-service",
    middleware=[
        LoggingMiddleware()
    ]
)

load_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000)
