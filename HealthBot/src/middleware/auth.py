from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from src.routers.user import registration_start
from src.api.handlers import get_user_by_id, get_all_doctors


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if await get_user_by_id(event.chat.id) or await data['state'].get_data():
            return await handler(event, data)
        else:
            await registration_start(event, state=data['state'])


class DoctorAuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.chat.id in await get_all_doctors():
            return await handler(event, data)
