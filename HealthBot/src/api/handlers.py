import logging
from os import getenv
from dotenv import load_dotenv
import aiohttp

load_dotenv()
API_HOST = getenv("API_HOST")
API_PORT = getenv("API_PORT")
API_URL = f"http://localhost:{API_PORT}"


async def add_user(data: dict) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL + "/users/", json=data) as response:
            return await response.json()


# TODO: add ttl cache
async def get_user_by_id(id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL + f"/users/{id}") as response:
            return await response.json()


async def update_user(user_id: int,
                      field: str,
                      new_data: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.patch(API_URL + f"/users/{user_id}",
                                 json={
                                     field: new_data
                                 }) as response:
            data = await response.json()
            if not data['success']:
                logging.error(f"User update error : {data['message']}")
            else:
                logging.info(f"Updated {user_id}, set {field} = {new_data}")


async def add_disease(disease_data: dict) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL + "/diseases/", json=disease_data) as response:
            return await response.json()


async def get_user_diseases(user_id: int) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL + f"/users/diseases/{user_id}") as response:
            return await response.json()
