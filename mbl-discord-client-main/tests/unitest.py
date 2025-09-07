import unittest
import asyncio
from tests.bridge import APIBridge

class TestAPI(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.api = APIBridge("http://127.0.0.1:8000") 

    async def test_get_dashboard(self):
        resp = await self.api.get("/dashboard")
        self.assertIsInstance(resp, dict)  # Pastikan return JSON dict
        self.assertIn("status", resp)      # Pastikan ada field 'status'

    async def test_post_login(self):
        resp = await self.api.post("/login", {"username": "test", "password": "1234"})
        self.assertIsInstance(resp, dict)
        self.assertIn("token", resp)

if __name__ == "__main__":
    unittest.main()
