import pytest


@pytest.mark.asyncio
async def test_add_notification(async_client, notifications_test_user):
    payload = {
        "user_id": notifications_test_user.id,
        "message": "Test notification",
        "start_date": "01.01.2025 09:00",
        "end_date": "01.01.2025 09:00",
        "is_patient": True,
        "time_notifications": [{"time": "09:00"}]
    }
    response = await async_client.post("/notifications/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Test notification"
    assert data["user_id"] == notifications_test_user.id


@pytest.mark.asyncio
async def test_get_all_notifications(async_client):
    response = await async_client.get("/notifications/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_notifications_for_user(async_client, notifications_test_user):
    response = await async_client.get(f"/notifications/for_user/{notifications_test_user.id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_doctor_schedule(async_client, notifications_test_user):
    # Добавим уведомление, подходящее по условиям
    payload = {
        "user_id": notifications_test_user.id,
        "message": "Doctor-only notification",
        "start_date": "05.05.2025 12:00",
        "end_date": "05.05.2025 12:00",
        "is_patient": False,
        "time_notifications": [{"time": "12:00"}]
    }
    await async_client.post("/notifications/", json=payload)

    response = await async_client.get(f"/notifications/schedule/{notifications_test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert all(not n["is_patient"] for n in data)


@pytest.mark.asyncio
async def test_delete_notification(async_client, notifications_test_user):
    # Сначала создадим
    payload = {
        "user_id": notifications_test_user.id,
        "message": "To be deleted",
        "start_date": "10.01.2025 08:00",
        "end_date": "10.01.2025 08:00",
        "is_patient": True,
        "time_notifications": [{"time": "08:00"}]
    }
    create_response = await async_client.post("/notifications/", json=payload)
    notification_id = create_response.json()["id"]

    response = await async_client.delete(f"/notifications/{notification_id}")
    assert response.status_code == 200
    assert response.json()["success"] is True


@pytest.mark.asyncio
async def test_add_notification_invalid_date(async_client, notifications_test_user):
    payload = {
        "user_id": notifications_test_user.id,
        "message": "Invalid date format",
        "start_date": "invalid-date",
        "end_date": "also-wrong",
        "is_patient": True,
        "time_notifications": [{"time": "09:00"}]
    }
    response = await async_client.post("/notifications/", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_add_notification_missing_required(async_client):
    response = await async_client.post("/notifications/", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_nonexistent_notification(async_client):
    response = await async_client.delete("/notifications/9999999")
    assert response.status_code == 200
    assert response.json()["success"] is True  # так как delete silent
