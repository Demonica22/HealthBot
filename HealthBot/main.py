import asyncio

from aiogram import Bot, Dispatcher
from os import getenv
from dotenv import load_dotenv

from src.handlers import routers
from src.startup import on_startup


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.startup.register(on_startup)

    for router in routers:
        dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    load_dotenv()
    TOKEN = getenv("BOT_TOKEN")
    asyncio.run(main())
