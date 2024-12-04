from os import getenv
from dotenv import load_dotenv
import aiohttp

load_dotenv()
API_HOST = getenv("API_HOST")
API_PORT = getenv("API_PORT")
API_URL = f"http://{API_HOST}:{API_PORT}"


async def add_user(data: dict) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL + "/users/", json=data) as response:
            return await response.json()


async def get_user_by_id(id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL + f"/users/{id}") as response:
            return await response.json()
