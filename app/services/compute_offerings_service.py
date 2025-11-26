from helpers.http_client import get_json

class ComputeService:

    async def get_compute_offerings(self, base_url:str, zoneUuid: str, lang: str, headers: dict):
        url = f"{base_url}/restapi/costestimate/compute-plan-list"
        
        params = {
            "zoneUuid": zoneUuid,
            "computeOfferingType": "PAY_AS_YOU_GO",
            "lang": lang
        }

        return await get_json(url, params, headers)

    async def get_vpn_user_cost(self, base_url:str, headers: dict):
        url = f"{base_url}/restapi/costestimate/vpn-user-cost"
        
        data = await get_json(url, headers=headers)
        return { "data": data }
