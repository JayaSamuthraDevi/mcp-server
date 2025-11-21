from fastmcp import FastMCP
import httpx
from config import (
    STACKBILL_API_KEY,
    STACKBILL_SECRET_KEY,
    STACKBILL_BASE_URL,
)

# Initialize the FastMCP server with a name
mcp = FastMCP("mcp-service")

@mcp.tool()
async def get_compute_offerings(
    zoneUuid: str,
    lang: str = "en",
) -> dict:

    # Build the API URL
    url =  f"{STACKBILL_BASE_URL}/restapi/costestimate/compute-plan-list"

    params = {
        "zoneUuid": zoneUuid,
        "computeOfferingType": "PAY_AS_YOU_GO",
        "lang": lang
    }

    # Build headers with authentication if provided
    headers = {
    "apikey": STACKBILL_API_KEY,
    "secretkey": STACKBILL_SECRET_KEY
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers, timeout=30.0)
            response.raise_for_status()
            return {
                "status": "success",
                "data": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                "zone_id": zoneUuid
            }
    except httpx.HTTPError as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to fetch usage cost details: {str(e)}"
        }

# Run the server using the "streamable-http" transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000)