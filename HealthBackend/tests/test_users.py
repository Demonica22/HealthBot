import random

import pytest
from fastapi import status
from sqlalchemy import select
from tests import conftest
from src.users.models import User

@pytest.mark.asyncio()
async def test_create_user(db_session, async_client):
    data = {
        "id": 111,
        "name": "Test",
        "gender": "test",
        "language": "ru",
        "weight": 100,
        "height": 120
    }
    response = await async_client.post("/users/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data == data

@pytest.mark.asyncio
async def test_get_user(async_client):
    data = {
        "id": 2,
        "name": "Another",
        "gender": "female",
        "language": "ru",
        "weight": 60,
        "height": 170
    }
    await async_client.post("/users/", json=data)

    response = await async_client.get("/users/2")
    assert response.status_code == 200
    assert response.json()["name"] == "Another"

@pytest.mark.asyncio
async def test_get_all_users(async_client):
    response = await async_client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_all_users_with_filters(async_client):
    response = await async_client.get("/users/?with_diseases=true&free=true")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_user(async_client):
    data = {
        "id": 3,
        "name": "PatchMe",
        "gender": "male",
        "language": "en",
        "weight": 85,
        "height": 175
    }
    await async_client.post("/users/", json=data)

    patch = {"name": "Updated Name", "doctor_id": 0}  # сбрасываем врача

    response = await async_client.patch("/users/3", json=patch)
    assert response.status_code == 200
    assert response.json()["success"] is True

@pytest.mark.asyncio
async def test_get_users_by_doctor(async_client):
    # создаём пользователя с doctor_id
    data = {
        "id": 4,
        "name": "WithDoctor",
        "gender": "female",
        "language": "ru",
        "weight": 55,
        "height": 165
    }
    doctor_data = {
        "id": 101,
        "name": "Doctor",
        "gender": "female",
        "language": "ru",
        "weight": 55,
        "height": 165
    }
    created_user = await async_client.post("/users/", json=data)
    created_doctor = await async_client.post("/users/", json=doctor_data)
    response = await async_client.patch("/users/4", json={"doctor_id": 101})
    assert response.json()['success'] is True
    response = await async_client.get("/users/by_doctor/101")
    assert response.status_code == 200
    users = response.json()
    assert any(u["id"] == 4 for u in users)

@pytest.mark.asyncio
async def test_partial_update_user(async_client):
    data = {
        "id": 6,
        "name": "Partial",
        "gender": "female",
        "language": "ru",
        "weight": 60,
        "height": 165
    }
    await async_client.post("/users/", json=data)

    patch = {"language": "en"}
    response = await async_client.patch("/users/6", json=patch)
    assert response.status_code == 200

    user = await async_client.get("/users/6")
    assert user.status_code == 200
    assert user.json()["language"] == "en"

@pytest.mark.asyncio
async def test_reset_doctor_id_to_none(async_client):
    data = {
        "id": 7,
        "name": "WithDoc",
        "gender": "male",
        "language": "en",
        "weight": 75,
        "height": 175
    }
    await async_client.post("/users/", json=data)

    response = await async_client.patch("/users/7", json={"doctor_id": 101})
    assert response.json()['success'] is True
    # Сброс
    response = await async_client.patch("/users/7", json={"doctor_id": 0})
    assert response.status_code == 200
    assert response.json()["success"] is True
