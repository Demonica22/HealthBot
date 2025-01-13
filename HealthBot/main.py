import asyncio

from aiogram import Bot, Dispatcher
from os import getenv
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.handlers import routers
from src.startup import on_startup
from src.custom_logging import LoggingMiddleware


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.message.middleware(LoggingMiddleware())

    for router in routers:
        dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    load_dotenv()
    TOKEN = getenv("BOT_TOKEN")
    asyncio.run(main())
