from src.database.main import initialize_database
from src.custom_logging import setup_logging


async def on_startup() -> None:
    await setup_logging()
    await initialize_database()
