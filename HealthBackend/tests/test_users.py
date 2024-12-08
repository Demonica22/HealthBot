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
    # user = User(**data)
    # db_session.add(user)
    #
    # await db_session.commit()

    response = await async_client.post("/users/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data == data
