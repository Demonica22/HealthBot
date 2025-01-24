import asyncio

from aiogram import Bot, Dispatcher
from os import getenv
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.routers import routers
from src.lifespan import on_startup, on_shutdown
from src.middleware.logging import LoggingMiddleware
from src.middleware.auth import AuthMiddleware

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(AuthMiddleware())
    for router in routers:
        dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    load_dotenv()
    TOKEN = getenv("BOT_TOKEN")
    asyncio.run(main())
