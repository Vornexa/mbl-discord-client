import aiohttp
import os


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


async def login(username: str, password: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE_URL}/login", json={"username": username, "password": password}
        ) as resp:
            return await resp.json()
    
async def get_dashboard():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/dashboard") as resp:
            return await resp.json()
        
async def get_jadwal_pengganti():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/jadwal/pengganti") as resp:
            return await resp.json()
        
async def get_jadwal_ujian():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/jadwal/ujian") as resp:
            return await resp.json()
        
async def post_cek_lokasi(data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE_URL}/cek-lokasi", json=data
        ) as resp:
            return await resp.json()