from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, URLInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, F

from src.api.handlers import get_user_by_id, get_free_users, get_doctor_patients, update_user,get_user_diseases_url
from src.localizations.main import get_text
from src.middleware.auth import DoctorAuthMiddleware
from src.utils.message_formatters import generate_users_message
from src.states.doctor_choose_patient import FreePatientChoose, DoctorsPatientChoose
from src.states.disease_add import DiseaseAdd

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
async def doctor_menu_callback_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
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
            callback_data="choose_free_patient")])

    buttons.append([InlineKeyboardButton(
        text=get_text("doctor_menu_button", user_language),
        callback_data="doctor_menu")])
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(generate_users_message(free_users, user_language, 'free'),
                                     reply_markup=inline_keyboard)


@doctor_router.callback_query(F.data == "choose_free_patient")
async def choose_patient_handler(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    await state.set_state(FreePatientChoose.patient_id)
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
    await callback.message.edit_text(get_text("choose_patient_message", user_language), reply_markup=inline_keyboard)


@doctor_router.callback_query(FreePatientChoose.patient_id)
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


@doctor_router.callback_query(F.data == "get_patients")
async def get_patients(callback: CallbackQuery):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    patients = await get_doctor_patients(callback.message.chat.id)

    buttons: list[list[InlineKeyboardButton]] = []
    if not patients:
        buttons.append([InlineKeyboardButton(
            text=get_text("doctor_get_free_patients_button", user_language),
            callback_data="get_free_patients")])
    else:
        buttons.append([InlineKeyboardButton(
            text=get_text("doctor_choose_patient_button", user_language),
            callback_data="choose_doctor_patient")])
    buttons.append([InlineKeyboardButton(
        text=get_text("doctor_menu_button", user_language),
        callback_data="doctor_menu")])
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(generate_users_message(patients, user_language, 'mine'),
                                     reply_markup=inline_keyboard)


@doctor_router.callback_query(F.data == "choose_doctor_patient")
async def choose_doctor_patient_handler(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    await state.set_state(DoctorsPatientChoose.patient_id)
    patients = await get_doctor_patients(callback.message.chat.id)

    buttons: list[list[InlineKeyboardButton]] = [
    ]
    for user in patients:
        buttons.append([InlineKeyboardButton(text=user['name'], callback_data=str(user['id']))])
    back_button = [
        InlineKeyboardButton(
            text=get_text("back_button", user_language),
            callback_data="back_doctors_patients")
    ]
    buttons.append(back_button)
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(get_text("choose_patient_message", user_language),
                                     reply_markup=inline_keyboard)


@doctor_router.callback_query(DoctorsPatientChoose.patient_id)
async def choose_doctor_patient_id_handler(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    id_ = callback.data
    patient = await get_user_by_id(int(id_))
    await state.update_data(patient_id=id_)
    await state.set_state(DoctorsPatientChoose.action)
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(
            text=get_text("add_disease_for_patient_button", user_language),
            callback_data="add_disease_for_patient")],
        [InlineKeyboardButton(
            text=get_text("add_appointment_for_patient_button", user_language),
            callback_data="add_appointment_for_patient")],
        [InlineKeyboardButton(
            text=get_text("get_patient_medical_card_button", user_language),
            callback_data="get_patient_medical_card")],
        [InlineKeyboardButton(
            text=get_text("back_button", user_language),
            callback_data="back_choose_doctors_patient")],
        [InlineKeyboardButton(
            text=get_text("doctor_menu_button", user_language),
            callback_data="doctor_menu")],
    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        get_text("patient_actions_message", lang=user_language).format(patient['name']),
        reply_markup=inline_keyboard)


@doctor_router.callback_query(F.data == "get_patient_medical_card")
async def get_patient_medical_card(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    patient_id = (await state.get_data())["patient_id"]

    file = URLInputFile(
        await get_user_diseases_url(user_id=patient_id,
                                    period_for_load=-1, # -1 потому что всегда получаем полную карточку
                                    user_language=user_language,
                                    response_format="docx"),
        filename=get_text("diseases_filename", user_language)
    )
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text=get_text("doctor_menu_button", user_language),
                              callback_data="doctor_menu")]
    ])
    await callback.message.delete()

    await callback.message.answer_document(caption=get_text("get_patient_medical_card_message", user_language),
                                           document=file)
    await callback.message.answer(get_text("what_is_next", user_language),
                                  reply_markup=inline_keyboard)


@doctor_router.callback_query(DoctorsPatientChoose.action and F.data == "add_disease_for_patient")
async def choose_doctor_patient_id_handler(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']

    await callback.message.answer(get_text("add_disease_message", user_language))
    patient_id = (await state.get_data())["patient_id"]
    await state.clear()

    await state.set_state(DiseaseAdd.title)
    await state.update_data(for_patient=patient_id)
