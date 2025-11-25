from services.compute_offerings_service import ComputeService
from exceptions.exception_handler import wrap_tool_exceptions

service = ComputeService()

def register(mcp):

    @mcp.tool()
    @wrap_tool_exceptions("Failed to fetch compute offerings")
    async def get_compute_offerings(
        zoneUuid: str,
        lang: str = "en",
        credentials: dict | None = None
    ) -> dict:

        c = credentials["stackbill"]

        headers = {
            "apikey": c["api_key"],
            "secretkey": c["secret_key"]
        }

        data = await service.get_compute_offerings(zoneUuid, lang, headers)

        return {
            "status": "success",
            "zone_id": zoneUuid,
            "data": data
        }

    @mcp.tool()
    @wrap_tool_exceptions("Failed to fetch VPN user cost")
    async def get_vpn_user_cost(
        credentials: dict | None = None
    ) -> dict:

        c = credentials["stackbill"]

        headers = {
            "apikey": c["api_key"],
            "secretkey": c["secret_key"]
        }

        res = await service.get_vpn_user_cost(headers)

        return {
            "status": "success",
            **res
        }
