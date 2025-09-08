import os
from dotenv import load_dotenv


load_dotenv()


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


API_ENDPOINTS = {
    "login": f"{API_BASE_URL}/login",
    "dashboard": f"{API_BASE_URL}/dashboard",
    "jadwal_pengganti": f"{API_BASE_URL}/jadwal/pengganti",
    "jadwal_ujian": f"{API_BASE_URL}/jadwal/ujian",
    "cek_lokasi": f"{API_BASE_URL}/cek-lokasi",
}