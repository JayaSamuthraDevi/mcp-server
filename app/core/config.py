import os
from dotenv import load_dotenv

load_dotenv()

STACKBILL_API_KEY = os.getenv("STACKBILL_API_KEY")
STACKBILL_SECRET_KEY = os.getenv("STACKBILL_SECRET_KEY")
STACKBILL_BASE_URL = os.getenv("STACKBILL_BASE_URL")
STACKBILL_ZONEUUID = os.getenv("STACKBILL_ZONEUUID")

if not STACKBILL_API_KEY or not STACKBILL_SECRET_KEY:
    raise RuntimeError("Stackbill API credentials missing in environment variables")
