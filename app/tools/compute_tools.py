from services.billing_service import BillingService

billing = BillingService()

async def get_compute_offerings(lang: str = "en"):
    return await billing.compute_offerings(lang)
