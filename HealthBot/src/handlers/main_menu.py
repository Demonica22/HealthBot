from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import Router, F

from src.localizations.main import get_text
from src.api.handlers import get_user_by_id

main_router = Router()


async def send_main_menu(message: Message, edit: bool = False):
    # TODO: check if user is none
    user_language: str = (await get_user_by_id(message.chat.id))['language']

    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(
            text=get_text("check_personal_data", user_language),
            callback_data="check_personal_data")],
        [InlineKeyboardButton(
            text=get_text("add_disease_button", user_language),
            callback_data="add_disease")],
        [InlineKeyboardButton(
            text=get_text("get_diseases_button", user_language),
            callback_data="get_diseases")],
    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    if edit:
        await message.edit_text(get_text("main_menu_message", user_language), reply_markup=inline_keyboard)
    else:
        await message.answer(get_text("main_menu_message", user_language), reply_markup=inline_keyboard)


@main_router.callback_query(F.data == "to_main_menu")
async def to_main_menu(callback: CallbackQuery):
    await send_main_menu(callback.message, edit=True)
