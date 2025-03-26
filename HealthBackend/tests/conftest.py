import pytest_asyncio
import pytest
import httpx
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select

from sqlalchemy import NullPool
from src.database.settings import settings
from src.database.models import Base
from src.users.models import User  # noqa
from src.diseases.models import Disease  # noqa
from src.notifications.models import Notification, NotificationTime  # noqa
from src.doctors.models import Doctor  # noqa

DATABASE_URL = settings.database_test_url

engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)
async_session = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with engine.connect() as connection:
        async with async_session(bind=connection) as session:
            yield session
            await session.rollback()


@pytest.fixture(scope="function")
def override_get_session(db_session):
    async def _override_get_session():
        yield db_session

    return _override_get_session


@pytest.fixture(scope="function")
def test_app(override_get_session):
    from src.database.session import get_session
    from main import app

    app.dependency_overrides[get_session] = override_get_session

    return app


@pytest_asyncio.fixture(scope="function")
async def async_client(test_app):
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=test_app),
                                 base_url="http://127.0.0.1:8000") as test_client:
        yield test_client


@pytest.fixture
async def disease_test_user(db_session):
    user_id = 999  # фиксированный ID для тестов

    result = await db_session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        user = User(
            id=user_id,
            name="DiseaseTestUser",
            gender="other",
            language="en",
            weight=70,
            height=170
        )
        db_session.add(user)
        await db_session.commit()

    return user


@pytest.fixture
async def test_doctor(db_session):
    doctor_id = 101
    result = await db_session.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalars().first()

    if not doctor:
        doctor = Doctor(id=doctor_id, name="Test Doctor")
        db_session.add(doctor)
        await db_session.commit()

    return doctor


@pytest.fixture
async def notifications_test_user(db_session):
    from src.users.models import User
    user_id = 4444
    result = await db_session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        user = User(
            id=user_id,
            name="NotificationUser",
            gender="other",
            language="en",
            weight=70,
            height=170
        )
        db_session.add(user)
        await db_session.commit()

    return user
