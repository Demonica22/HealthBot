import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_add_doctor(async_client):
    doctor_data = {"id": 777}
    response = await async_client.post("/doctor/", json=doctor_data)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == doctor_data["id"]


@pytest.mark.asyncio
async def test_get_all_doctors(async_client):
    # Добавим доктора для гарантии
    await async_client.post("/doctor/", json={"id": 778})

    response = await async_client.get("/doctor/")
    assert response.status_code == 200
    doctors = response.json()
    assert isinstance(doctors, list)
    assert 778 in doctors


@pytest.mark.asyncio
async def test_add_doctor_missing_id(async_client):
    response = await async_client.post("/doctor/", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_add_doctor_invalid_id_type(async_client):
    response = await async_client.post("/doctor/", json={"id": "not_an_int"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_doctors_empty(db_session, async_client):
    await db_session.execute(text("DELETE FROM doctors"))
    await db_session.commit()

    response = await async_client.get("/doctor/")
    assert response.status_code == 200
    assert response.json() == []
