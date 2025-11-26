import httpx
import logging
logger = logging.getLogger("mcp")

async def get_json(url: str, params: dict | None = None, headers: dict | None = None):
    safe_headers = {k: "***" if "key" in k.lower() else v for k, v in (headers or {}).items()}

    logger.debug({
        "event": "http_request",
        "url": url,
        "params": params,
        "headers": safe_headers,
    })

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                url,
                params=params,
                headers=headers,
            )

        raw_text = response.text

        logger.debug({
            "event": "http_response",
            "status": response.status_code,
            "url": str(response.request.url),
            # "response_text": raw_text,
        })

        response.raise_for_status()

        # JSON detection
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()

        return raw_text

    except httpx.HTTPError as e:
        logger.error({
            "event": "http_error",
            "url": url,
            "params": params,
            "headers": safe_headers,
            "error": str(e),
            "status_code": getattr(e.response, "status_code", None),
            "response_text": getattr(e.response, "text", None),
        })
        raise
