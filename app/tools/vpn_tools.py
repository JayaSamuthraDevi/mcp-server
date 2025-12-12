from services.billing_service import BillingService

billing = BillingService()

async def get_vpn_user_cost():
    return await billing.vpn_user_cost()
