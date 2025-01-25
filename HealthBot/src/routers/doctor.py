from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, F

from src.api.handlers import get_user_by_id, get_free_users, get_doctor_patients
from src.localizations.main import get_text
from src.middleware.auth import DoctorAuthMiddleware

doctor_router = Router()
doctor_router.message.middleware(DoctorAuthMiddleware())


@doctor_router.message(Command("doctor"))
async def doctor_menu(message: Message):
    user_language: str = (await get_user_by_id(message.chat.id))['language']

    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(
            text=get_text("doctor_get_patients", user_language),
            callback_data="get_patients")],
        [InlineKeyboardButton(
            text=get_text("doctor_get_free_patients", user_language),
            callback_data="get_free_patients")],
    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(get_text("doctor_menu", user_language), reply_markup=inline_keyboard)


@doctor_router.callback_query(F.data == "get_free_patients")
async def get_free_patients(callback: CallbackQuery):
    free_users = list(filter(lambda x: x['id'] != callback.message.chat.id, await get_free_users()))
    await callback.message.edit_text(", ".join(map(str, free_users)))


@doctor_router.callback_query(F.data == "get_patients")
async def get_patients(callback: CallbackQuery):
    patients = await get_doctor_patients(callback.message.chat.id)

    await callback.message.answer(", ".join(map(str, patients)) if patients else "zero")
