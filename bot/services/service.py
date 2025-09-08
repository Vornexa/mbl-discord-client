import aiohttp
import logging
import os

logger = logging.getLogger(__name__)

class APIService:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")

    async def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, **kwargs) as response:
                    response.raise_for_status()
                    data = await response.json()
                    logger.info(f"[API] {method} {url} ✅")
                    return data
        except aiohttp.ClientError as e:
            logger.error(f"[API] {method} {url} ❌ Error: {e}")
            return {"error": str(e)}

    async def get_dashboard(self, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        return await self._request("GET", "/dashboard", headers=headers)

    async def get_jadwal_pengganti(self, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        return await self._request("GET", "/jadwal/pengganti", headers=headers)

    async def get_jadwal_ujian(self, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        return await self._request("GET", "/jadwal/ujian", headers=headers)

    async def post_login(self, username: str, password: str):
        payload = {"username": username, "password": password}
        return await self._request("POST", "/login", json=payload)

    async def post_cek_lokasi(self, lokasi_id: int, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"lokasi_id": lokasi_id}
        return await self._request("POST", "/cek-lokasi", headers=headers, json=payload)
