from services.token_service import current_claims
from services.http_client import HttpService

http = HttpService()

class BillingService:

    async def compute_offerings(self, lang: str):
        claims = current_claims()

        url = f"{claims.base_url}/restapi/costestimate/compute-plan-list"
        params = {
            "zoneUuid": claims.zone_uuid,
            "computeOfferingType": "PAY_AS_YOU_GO",
            "lang": lang,
        }
        headers = {"apikey": claims.api_key, "secretkey": claims.secret_key}

        return await http.get(url, headers, params)

    async def vpn_user_cost(self):
        claims = current_claims()

        url = f"{claims.base_url}/restapi/costestimate/vpn-user-cost"
        headers = {"apikey": claims.api_key, "secretkey": claims.secret_key}

        return await http.get(url, headers)
