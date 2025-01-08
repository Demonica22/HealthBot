import logging
import aiohttp

from http import HTTPStatus
from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timedelta
from src.api.schemas import DiseaseSchema

load_dotenv()
API_HOST = getenv("API_HOST")
API_PORT = getenv("API_PORT")
API_URL = f"http://{API_HOST}:{API_PORT}"


async def add_user(data: dict) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL + "/users/", json=data) as response:
            return await response.json()


# TODO: add ttl cache
async def get_user_by_id(id: int) -> dict | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL + f"/users/{id}") as response:
            if response.status == HTTPStatus.NOT_FOUND:
                return None
            return await response.json()


async def update_user(user_id: int,
                      field: str,
                      new_data: str):
    async with aiohttp.ClientSession() as session:
        async with session.patch(API_URL + f"/users/{user_id}",
                                 json={
                                     field: new_data
                                 }) as response:
            data = await response.json()
            response.raise_for_status()
            logging.debug(f"Updated {user_id}, set {field} = {new_data}")


async def add_disease(disease_data: dict) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        logging.debug(f"Disease add: {disease_data}")
        async with session.post(API_URL + "/diseases/", json=disease_data) as response:
            response.raise_for_status()
            return await response.json()


async def get_user_diseases(user_id: int,
                            period_for_load: int = -1) -> list[dict]:
    if period_for_load == -1:
        start_date = -1
    else:
        start_date = (datetime.now() - timedelta(days=30 * period_for_load)).strftime("%d.%m.%Y")

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL + f"/users/diseases/{user_id}", params={'start_date': start_date}) as response:
            response.raise_for_status()
            diseases_list = await response.json()
            diseases_list[:] = [DiseaseSchema(**disease).model_dump() for disease in diseases_list]
            return diseases_list
