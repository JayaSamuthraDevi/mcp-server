from helpers.http_client import get_json
from config import STACKBILL_BASE_URL, STACKBILL_ZONEUUID

class ComputeService:

    async def get_compute_offerings(self, zoneUuid: str, lang: str, headers: dict):
        url = f"{STACKBILL_BASE_URL}/restapi/costestimate/compute-plan-list"
        
        params = {
            "zoneUuid": zoneUuid,
            "computeOfferingType": "PAY_AS_YOU_GO",
            "lang": lang
        }

        return await get_json(url, params, headers)

    async def get_vpn_user_cost(self, headers: dict):
        url = f"{STACKBILL_BASE_URL}/restapi/costestimate/vpn-user-cost"
        
        data = await get_json(url, headers=headers)
        return { "zone_id": STACKBILL_ZONEUUID, "data": data }
