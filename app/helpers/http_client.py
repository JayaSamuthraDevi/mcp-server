import httpx

async def get_json(url: str, params: dict | None = None, headers: dict | None = None):

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params=params,
            headers=headers,
            timeout=30.0
        )
        response.raise_for_status()

        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()

        return response.text
