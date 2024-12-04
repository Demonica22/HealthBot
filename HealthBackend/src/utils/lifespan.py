from contextlib import asynccontextmanager
from src.database.main import initialize_database


@asynccontextmanager
async def lifespan(app):
    await initialize_database()

    yield

    pass
