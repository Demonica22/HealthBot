import logging
import aiohttp
from urllib.parse import urlencode

from http import HTTPStatus
from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timedelta
from src.api.schemas import DiseaseSchema
from src.utils.timezone import MSK

load_dotenv()
API_HOST = getenv("API_HOST")
SERVER_HOST = getenv("SERVER_HOST")
API_PORT = getenv("API_PORT")
API_URL = f"http://{API_HOST}:{API_PORT}"
USERS_URL = API_URL + "/users/"
DISEASES_URL = API_URL + "/diseases/"
DISEASES_URL_FOR_USER = DISEASES_URL + "for_user/"
SERVER_URl = f"http://{SERVER_HOST}:{API_PORT}"
USER_DISEASES_SERVER_URL = SERVER_URl + "/diseases/" + "for_user/"
FINISH_DISEASE_URL = DISEASES_URL + "mark_as_finished/"
NOTIFICATIONS_URL = API_URL + "/notifications/"
NOTIFICATIONS_FOR_USER = NOTIFICATIONS_URL + "for_user/"


async def add_user(data: dict) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(USERS_URL, json=data) as response:
            return await response.json()


# TODO: add ttl cache
async def get_user_by_id(id: int) -> dict | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(USERS_URL + f"{id}") as response:
            if response.status == HTTPStatus.NOT_FOUND:
                return None
            return await response.json()


async def update_user(user_id: int,
                      field: str,
                      new_data: str):
    async with aiohttp.ClientSession() as session:
        async with session.patch(USERS_URL + f"{user_id}",
                                 json={
                                     field: new_data
                                 }) as response:
            data = await response.json()
            if not data['success']:
                raise Exception("Ошибка обновления данных пользователя")
            response.raise_for_status()
            logging.debug(f"Updated {user_id}, set {field} = {new_data}")


async def add_disease(disease_data: dict) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        logging.debug(f"Disease add: {disease_data}")
        async with session.post(DISEASES_URL, json=disease_data) as response:
            response.raise_for_status()
            return await response.json()


async def get_user_diseases(user_id: int,
                            period_for_load: int = -1) -> list[dict]:
    if period_for_load == -1:
        start_date = -1
    else:
        start_date = (datetime.now(MSK) - timedelta(days=30 * period_for_load)).strftime("%d.%m.%Y")

    async with aiohttp.ClientSession() as session:
        async with session.get(DISEASES_URL_FOR_USER + f"{user_id}", params={'start_date': start_date}) as response:
            response.raise_for_status()
            diseases_list = await response.json()
            diseases_list[:] = [DiseaseSchema(**disease).model_dump() for disease in diseases_list]
            return diseases_list


async def get_user_diseases_url(user_id: int,
                                period_for_load: int,
                                user_language: str,
                                response_format: str,

                                ) -> str:
    if period_for_load == -1:
        start_date = -1
    else:
        start_date = (datetime.now(MSK) - timedelta(days=30 * period_for_load)).strftime("%d.%m.%Y")
    return USER_DISEASES_SERVER_URL + f"{user_id}" + "?" + urlencode({'start_date': start_date,
                                                                      'response_format': response_format,
                                                                      'user_language': user_language
                                                                      })


async def get_user_active_diseases(user_id: int) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(DISEASES_URL_FOR_USER + f"{user_id}", params={'only_active': 1}) as response:
            response.raise_for_status()
            diseases_list = await response.json()
            diseases_list[:] = [DiseaseSchema(**disease).model_dump() for disease in diseases_list]
            return diseases_list


async def finish_disease(disease_id: int, update_date: datetime = None):
    async with aiohttp.ClientSession() as session:
        async with session.patch(FINISH_DISEASE_URL + f"{disease_id}") as response:
            response.raise_for_status()
            data = await response.json()
            if not data['success']:
                raise Exception("Ошибка завершения болезни")
            logging.debug(f"Болезнь {disease_id} помечена как завершенная")


async def get_disease(disease_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(DISEASES_URL + f"{disease_id}") as response:
            if response.status == HTTPStatus.NOT_FOUND:
                return None
            return await response.json()


async def add_notification(notification_data: dict) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        logging.debug(f"Notification add: {notification_data}")
        async with session.post(NOTIFICATIONS_URL, json=notification_data) as response:
            response.raise_for_status()
            return await response.json()


async def get_user_notifications(user_id: int) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(NOTIFICATIONS_FOR_USER + f"{user_id}") as response:
            response.raise_for_status()
            return await response.json()


async def delete_notification(notification_id: int) -> None:
    async with aiohttp.ClientSession() as session:
        logging.debug(f"Notification deleted: {notification_id}")
        async with session.delete(NOTIFICATIONS_URL + f"{notification_id}") as response:
            response.raise_for_status()
            data = await response.json()
            if not data['success']:
                raise Exception("Ошибка удаления уведомления")


async def get_all_notifications() -> list[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(NOTIFICATIONS_URL) as response:
            response.raise_for_status()
            return await response.json()
