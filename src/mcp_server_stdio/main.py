from fastmcp import FastMCP
from mcp_server_stdio.tools.loader import load_tools
import sys

def run():

    mcp = FastMCP(
        "mcp-service",
        middleware=[
        ]
    )
    load_tools(mcp)

    print("=" * 70, file=sys.stderr)
    print("Starting MCP Service Server", file=sys.stderr)
    print("Transport: stdio (MCP over stdin/stdout)", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
