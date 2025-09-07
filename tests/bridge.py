import aiohttp

class APIBridge:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get(self, endpoint: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}{endpoint}") as resp:
                return await resp.json()

    async def post(self, endpoint: str, data: dict):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}{endpoint}", json=data) as resp:
                return await resp.json()
