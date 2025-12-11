import logging
from typing import Any
from fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_access_token
import httpx
from core.keycloak import keycloak_auth

mcp = FastMCP(name="My Protected Server",   auth = keycloak_auth)

@mcp.tool()
def hello(context: Context) -> str:
    """Greet the authenticated user - similar to Gmail's approach"""
    token = get_access_token()  # returns TokenData
    claims = token.claims       # decoded JWT payload
    logging.info(f"User claims: {claims}")
    logging.info(f"Token: {token}")
    user_email = claims.get("email")
    user_name = claims.get("name")

    return f"Hello {user_name}! Email: {user_email}"

@mcp.tool()
async def get_compute_offerings(context: Context,lang:str ='en') -> dict[str, Any]:
    """Get compute offerings for the authenticated user"""
    token = get_access_token()  # returns TokenData
    claims = token.claims       # decoded JWT payload
    base_url = claims.get("base_url")
    zone_uuid = claims.get("zone_uuid")
    api_key = claims.get("api_key")
    secret_key = claims.get("secret_key")
    url = f"{base_url}/restapi/costestimate/compute-plan-list"
    params = {
            "zoneUuid": zone_uuid,
            "computeOfferingType": "PAY_AS_YOU_GO",
            "lang": lang,
        }
    headers = {
            "apikey": api_key,
            "secretkey": secret_key,
        }
    async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                url,
                params=params,
                headers=headers,
            )
    response.raise_for_status()

        # Parse JSON if content-type indicates JSON
    content_type = response.headers.get("content-type", "")
    if content_type.startswith("application/json"):
        return response.json()

    return {
            "status": "success",
            "data": response.text,
        }


@mcp.tool()
async def get_vpn_user_cost(context: Context) -> dict[str, Any]:
    """Get VPN user cost for the authenticated user"""
    token = get_access_token()  # returns TokenData
    claims = token.claims       # decoded JWT payload
    base_url = claims.get("base_url")
    api_key = claims.get("api_key")
    secret_key = claims.get("secret_key")
    headers = {
            "apikey": api_key,
            "secretkey": secret_key,
        }
    url = f"{base_url}/restapi/costestimate/vpn-user-cost"
    async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                url,
                headers=headers,
            )
    response.raise_for_status()

        # Parse JSON if content-type indicates JSON
    content_type = response.headers.get("content-type", "")
    if content_type.startswith("application/json"):
        return response.json()

    return {
            "status": "success",
            "data": response.text,
        }

mcp_http_app = mcp.http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:mcp_http_app", host="0.0.0.0", port=8000)
