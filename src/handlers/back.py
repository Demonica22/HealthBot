from .user import change_info
from aiogram import Router
from aiogram.types import CallbackQuery

back_router = Router()


@back_router.callback_query(lambda call: call.data.startswith("back"))
async def get_back(callback: CallbackQuery):
    previous_position: str = "_".join(callback.data.split("_")[1:])
    back_dict: dict[str:callable] = {
        "change_info": change_info
    }

    await back_dict[previous_position](callback)
