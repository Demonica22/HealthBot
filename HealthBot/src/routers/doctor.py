from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, F

from src.api.handlers import get_user_by_id, get_free_users, get_doctor_patients, update_user
from src.localizations.main import get_text
from src.middleware.auth import DoctorAuthMiddleware
from src.utils.message_formatters import generate_users_message
from src.states.doctor_choose_patient import PatientChoose

doctor_router = Router()
doctor_router.message.middleware(DoctorAuthMiddleware())


@doctor_router.message(Command("doctor"))
async def doctor_menu(message: Message, edit: bool = False):
    user_language: str = (await get_user_by_id(message.chat.id))['language']

    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(
            text=get_text("doctor_get_patients_button", user_language),
            callback_data="get_patients")],
        [InlineKeyboardButton(
            text=get_text("doctor_get_free_patients_button", user_language),
            callback_data="get_free_patients")],
    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    func = message.answer
    if edit:
        func = message.edit_text
    await func(get_text("doctor_menu", user_language), reply_markup=inline_keyboard)


@doctor_router.callback_query(F.data == "doctor_menu")
async def doctor_meny_callback_handler(callback: CallbackQuery):
    await doctor_menu(callback.message, edit=True)


@doctor_router.callback_query(F.data == "get_free_patients")
async def get_free_patients(callback: CallbackQuery):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    free_users = list(filter(lambda x: x['id'] != callback.message.chat.id, await get_free_users()))
    buttons: list[list[InlineKeyboardButton]] = [
    ]
    if free_users:
        buttons.append([InlineKeyboardButton(
            text=get_text("doctor_choose_patient_button", user_language),
            callback_data="choose_patient")])

    buttons.append([InlineKeyboardButton(
        text=get_text("doctor_menu_button", user_language),
        callback_data="doctor_menu")])
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(generate_users_message(free_users, user_language, 'free'),
                                     reply_markup=inline_keyboard)


@doctor_router.callback_query(F.data == "get_patients")
async def get_patients(callback: CallbackQuery):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    patients = await get_doctor_patients(callback.message.chat.id)

    buttons: list[list[InlineKeyboardButton]] = []
    if not patients:
        buttons.append([InlineKeyboardButton(
            text=get_text("doctor_get_free_patients_button", user_language),
            callback_data="get_free_patients")])

    buttons.append([InlineKeyboardButton(
        text=get_text("doctor_menu_button", user_language),
        callback_data="doctor_menu")])
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(generate_users_message(patients, user_language, 'mine'),
                                     reply_markup=inline_keyboard)


@doctor_router.callback_query(F.data == "choose_patient")
async def choose_patient_handler(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    await state.set_state(PatientChoose.patient_id)
    free_users = list(filter(lambda x: x['id'] != callback.message.chat.id, await get_free_users()))

    buttons: list[list[InlineKeyboardButton]] = [
    ]
    for user in free_users:
        buttons.append([InlineKeyboardButton(text=user['name'], callback_data=str(user['id']))])
    back_button = [
        InlineKeyboardButton(
            text=get_text("back_button", user_language),
            callback_data="back_free_patients")
    ]
    buttons.append(back_button)
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text("Выберите пациента:", reply_markup=inline_keyboard)


@doctor_router.callback_query(PatientChoose.patient_id)
async def choose_patient_id_handler(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    id_ = callback.data
    patient = await get_user_by_id(int(id_))
    await state.update_data(patient_id=id_)
    await update_user(user_id=int(id_),
                      field='doctor_id',
                      new_data=str(callback.message.chat.id))
    buttons: list[list[InlineKeyboardButton]] = [

        [InlineKeyboardButton(
            text=get_text("doctor_menu_button", user_language),
            callback_data="doctor_menu")],
    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        get_text("patient_choose_success_message", lang=user_language).format(patient['name']),
        reply_markup=inline_keyboard)
