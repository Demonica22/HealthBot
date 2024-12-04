from src.custom_logging import setup_logging


async def on_startup() -> None:
    await setup_logging()
