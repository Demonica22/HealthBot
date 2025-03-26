import pytest


@pytest.mark.asyncio
async def test_add_disease(async_client, disease_test_user):
    response = await async_client.post("/diseases/", json={
        "user_id": disease_test_user.id,
        "description": "Test disease",
        "date_from": "01.01.2024",
        "date_to": "10.01.2024",
        "still_sick": False,
        "title": "Flu",
        "treatment_plan": "Rest and fluids"
    })
    assert response.status_code == 201
    result = response.json()
    assert result["title"] == "Flu"
@pytest.mark.asyncio
async def test_get_disease(async_client, disease_test_user):
    create_response = await async_client.post("/diseases/", json={
        "user_id": disease_test_user.id,
        "description": "Headache",
        "date_from": "02.02.2024",
        "date_to": "03.02.2024",
        "still_sick": False,
        "title": "Migraine",
        "treatment_plan": "Painkillers"
    })
    disease_id = create_response.json()["id"]

    response = await async_client.get(f"/diseases/{disease_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Migraine"

@pytest.mark.asyncio
async def test_mark_disease_as_finished(async_client, disease_test_user):
    create_response = await async_client.post("/diseases/", json={
        "user_id": disease_test_user.id,
        "description": "Cough",
        "date_from": "05.02.2024",
        "still_sick": True,
        "title": "Cold",
        "treatment_plan": None
    })
    disease_id = create_response.json()["id"]

    response = await async_client.patch(f"/diseases/mark_as_finished/{disease_id}")
    assert response.status_code == 200
    assert response.json()["success"] is True

@pytest.mark.asyncio
async def test_get_all_user_diseases(async_client, disease_test_user):
    await async_client.post("/diseases/", json={
        "user_id": disease_test_user.id,
        "description": "Infection",
        "date_from": "01.01.2024",
        "still_sick": True,
        "title": "Infection",
        "treatment_plan": "Antibiotics"
    })

    response = await async_client.get(f"/diseases/for_user/{disease_test_user.id}")
    assert response.status_code == 200
    assert any(d["title"] == "Infection" for d in response.json())

@pytest.mark.asyncio
async def test_get_diseases_with_start_date_excludes_old(async_client, disease_test_user):
    # старое
    await async_client.post("/diseases/", json={
        "user_id": disease_test_user.id,
        "description": "Old illness",
        "date_from": "01.01.2023",
        "date_to": "10.01.2023",
        "still_sick": False,
        "title": "OldFlu",
        "treatment_plan": None
    })

    # новое
    await async_client.post("/diseases/", json={
        "user_id": disease_test_user.id,
        "description": "New illness",
        "date_from": "01.01.2025",
        "date_to": "10.01.2025",
        "still_sick": False,
        "title": "NewFlu",
        "treatment_plan": None
    })

    response = await async_client.get(
        f"/diseases/for_user/{disease_test_user.id}?start_date=01.01.2024"
    )
    assert response.status_code == 200
    titles = [d["title"] for d in response.json()]
    assert "OldFlu" not in titles
    assert "NewFlu" in titles
