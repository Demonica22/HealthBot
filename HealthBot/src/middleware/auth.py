from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from src.routers.user import registration_start
from src.api.handlers import get_user_by_id


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if await get_user_by_id(event.chat.id):
            return await handler(event, data)
        else:
            await registration_start(event, state=data['state'])
