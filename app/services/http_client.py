import httpx

class HttpService:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    async def get(self, url: str, headers: dict, params: dict | None = None):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return self._parse(response)

    def _parse(self, response: httpx.Response):
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return {"status": "success", "data": response.text}
