from src.database.session import engine
from src.database.models import Base


async def initialize_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
