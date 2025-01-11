from src.handlers.user import get_info
from src.handlers.main_menu import to_main_menu
from src.handlers.disease import get_active_diseases
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

back_router = Router()


@back_router.callback_query(lambda call: call.data.startswith("back"))
async def get_back(callback: CallbackQuery, state: FSMContext):
    previous_position: str = "_".join(callback.data.split("_")[1:])
    back_dict: dict[str:callable] = {
        "check_info": get_info,
        "diseases_menu": to_main_menu,
        "diseases_mark": get_active_diseases
    }
    await state.clear()
    await back_dict[previous_position](callback)
