import inspect
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.routers.user import get_info
from src.routers.main_menu import to_main_menu
from src.routers.disease import get_active_diseases
from src.routers.notifications import get_all_notifications, notifications_delete, notification_menu
from src.routers.doctor import get_free_patients

back_router = Router()


@back_router.callback_query(lambda call: call.data.startswith("back"))
async def get_back(callback: CallbackQuery, state: FSMContext):
    previous_position: str = "_".join(callback.data.split("_")[1:])
    back_dict: dict[str:callable] = {
        "check_info": get_info,
        "diseases_menu": to_main_menu,
        "notifications_menu": notification_menu,
        "notifications_delete": get_all_notifications,
        "notification_deleted": notifications_delete,
        "diseases_mark": get_active_diseases,
        "free_patients": get_free_patients,
    }
    await state.clear()  # не добавлять back не на первую итерацию state
    if "state" in inspect.getfullargspec(back_dict[previous_position]).args:
        await back_dict[previous_position](callback, state)
    else:
        await back_dict[previous_position](callback)
