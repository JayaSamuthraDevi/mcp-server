from fastmcp import Context
from services.compute_offerings_service import ComputeService
from exceptions.exception_handler import wrap_tool_exceptions

service = ComputeService()

def register(mcp):

    @mcp.tool()
    @wrap_tool_exceptions("Failed to fetch compute offerings")
    async def get_compute_offerings(
        context: Context,
        lang: str = "en"
    ) -> dict:
        """
        Fetch compute offerings from Stackbill API.
        Credentials are automatically loaded from mcp.json via authentication middleware.
        """

        # Get credentials from context state (set by AuthMiddleware using set_state)
        base_url = context.get_state("base_url")
        zone_uuid = context.get_state("zone_uuid")
        api_key = context.get_state("api_key")
        secret_key = context.get_state("secret_key")

        headers = {
            "apikey": api_key,
            "secretkey": secret_key
        }

        data = await service.get_compute_offerings(base_url, zone_uuid, lang, headers)

        return {
            "status": "success",
            "zone_id": zone_uuid,
            "data": data
        }

    @mcp.tool()
    @wrap_tool_exceptions("Failed to fetch VPN user cost")
    async def get_vpn_user_cost(
        context: Context
    ) -> dict:
        """
        Fetch VPN user cost from Stackbill API.
        Credentials are automatically loaded from mcp.json via authentication middleware.
        """

        # Get credentials from context state (set by AuthMiddleware using set_state)
        base_url = context.get_state("base_url")
        api_key = context.get_state("api_key")
        secret_key = context.get_state("secret_key")

        headers = {
            "apikey": api_key,
            "secretkey": secret_key
        }

        res = await service.get_vpn_user_cost(base_url, headers)

        return {
            "status": "success",
            **res
        }
