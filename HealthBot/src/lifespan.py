from src.custom_logging import setup_logging
from src.scheduler.main import start_up as start_up_scheduler


async def on_startup(bot) -> None:
    await setup_logging()
    await start_up_scheduler(bot)


async def on_shutdown() -> None:
    pass
