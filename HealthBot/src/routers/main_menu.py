from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Router, F

from src.localizations import get_text
from src.api.handlers import get_user_by_id
from src.utils.chat_keyboard_clearer import remove_chat_buttons

main_router = Router()


async def send_main_menu(message: Message, edit: bool = False):
    # TODO: check if user is none
    user_language: str = (await get_user_by_id(message.chat.id))['language']

    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(
            text=get_text("add_disease_button", user_language),
            callback_data="add_disease")],
        [InlineKeyboardButton(
            text=get_text("get_active_diseases_button", user_language),
            callback_data="get_active_diseases")],
        [InlineKeyboardButton(
            text=get_text("get_diseases_button", user_language),
            callback_data="get_diseases")],
        [InlineKeyboardButton(
            text=get_text("notifications_main_menu_button", user_language),
            callback_data="make_notification")],
        [InlineKeyboardButton(
            text=get_text("check_personal_data_button", user_language),
            callback_data="check_personal_data")],
    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    if edit:
        await message.edit_text(get_text("main_menu_message", user_language), reply_markup=inline_keyboard)
    else:
        await message.answer(get_text("main_menu_message", user_language), reply_markup=inline_keyboard)


@main_router.callback_query(F.data == "to_main_menu")
async def to_main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()  # FIXME: надо ли? не ломает ли?
    await send_main_menu(callback.message, edit=True)


@main_router.message(Command("exit"))
@main_router.message(Command("menu"))
async def cancel_operation(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']

    await state.clear()
    await remove_chat_buttons(message, user_language)
    await send_main_menu(message)
