import logging
from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import Message


async def setup_logging():
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    logging.basicConfig(
        level=logging.INFO, format=format, datefmt="[%X]", handlers=[logging.StreamHandler()]
    )


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        logging.info(f"Message handled by {data['handler'].callback.__name__}")
        return await handler(event, data)
