import re
import logging
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, URLInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Router, F

from src.api.handlers import (
    get_user_by_id,
    get_free_users,
    get_doctor_patients,
    update_user,
    get_user_diseases_url,
    add_notification,
    get_user_active_diseases,
    finish_disease,
    get_disease
)
from src.scheduler.utils import schedule_notifications, schedule_doctor_visit
from src.localizations.main import get_text
from src.middleware.auth import DoctorAuthMiddleware
from src.utils.message_formatters import generate_users_message, generate_active_diseases_message
from src.states.doctor_choose_patient import FreePatientChoose, DoctorsPatientChoose
from src.states.disease_add import DiseaseAdd
from src.states.doctor_appointment_add import DoctorAddAppointment
from src.utils.regex import DATE_REGEX, TIME_REGEX

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


@doctor_router.callback_query(DoctorsPatientChoose.patient_id and F.data.isdigit())
async def choose_doctor_patient_id_handler(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    id_ = callback.data
    patient = await get_user_by_id(int(id_))
    diseases = await get_user_active_diseases(int(id_))

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
            text=get_text("drop_patient_button", user_language),
            callback_data="drop_patient")],
        [InlineKeyboardButton(
            text=get_text("back_button", user_language),
            callback_data="back_choose_doctors_patient")],
        [InlineKeyboardButton(
            text=get_text("doctor_menu_button", user_language),
            callback_data="doctor_menu")],
    ]
    if diseases:
        buttons.insert(1,
                       [InlineKeyboardButton(
                           text=get_text("end_disease_for_patient_button", user_language),
                           callback_data="end_disease_for_patient")]
                       )
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        get_text("patient_actions_message", lang=user_language).format(patient['name']),
        reply_markup=inline_keyboard)


@doctor_router.callback_query(F.data == "end_disease_for_patient")
async def doctor_choose_disease_to_finish(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    patient_id = (await state.get_data())["patient_id"]
    buttons = [

        [InlineKeyboardButton(text=get_text("back_button", user_language),
                              callback_data=f"{patient_id}")],

    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        diseases = await get_user_active_diseases(patient_id)
    except Exception as x:
        logging.error(f"Ошибка получения активных болезней: {x}")
        await callback.message.answer(text=get_text("unexpected_error", user_language).format(x),
                                      reply_markup=inline_keyboard)
        return
    for i, disease in enumerate(diseases):
        button = [InlineKeyboardButton(text=f"№{i + 1} {disease['title']}",
                                       callback_data=f"doctor_disease_id_{disease['id']}")]
        buttons.insert(i, button)

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        get_text("diseases_choose_to_finish", user_language) + generate_active_diseases_message(diseases,
                                                                                                user_language),
        reply_markup=inline_keyboard)


@doctor_router.callback_query(F.data.startswith("doctor_disease_id"))
async def mark_disease_as_finished(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    patient_id = (await state.get_data())["patient_id"]

    disease_id = int(callback.data.split("_")[-1])
    buttons = [
        [InlineKeyboardButton(text=get_text("back_button", user_language),
                              callback_data="end_disease_for_patient")],
        [InlineKeyboardButton(text=get_text("back_to_patient_menu_button", user_language),
                              callback_data=f"{patient_id}")],
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await finish_disease(disease_id)
    except Exception as x:
        logging.error(f"Ошибка завершения болезни: {x}")
        await callback.message.answer(text=get_text("unexpected_error", user_language).format(x),
                                      reply_markup=inline_keyboard)
        return
    disease = await get_disease(disease_id)

    await callback.message.edit_text(get_text("diseases_finished_message", user_language).format(disease['title']),
                                     reply_markup=inline_keyboard)


@doctor_router.callback_query(DoctorsPatientChoose.action and F.data == "drop_patient")
async def make_sure_to_drop_patient(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    patient = await get_user_by_id((await state.get_data())["patient_id"])
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text=get_text("yes", user_language),
                              callback_data=f"sure_to_drop_patient")],
        [InlineKeyboardButton(text=get_text("back_to_patient_menu_button", user_language),
                              callback_data=f"{patient['id']}")],
    ])
    await state.set_state(DoctorsPatientChoose.patient_id)
    await callback.message.edit_text(get_text("sure_to_drop_patient_message", user_language)
                                     .format(patient['name']),
                                     reply_markup=inline_keyboard
                                     )


@doctor_router.callback_query(F.data == "sure_to_drop_patient")
async def drop_patient(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    patient_id = (await state.get_data())["patient_id"]
    patient = await get_user_by_id(int(patient_id))
    await update_user(
        user_id=int(patient_id),
        field='doctor_id',
        new_data=0  # cтавим 0, потому что если поставить None апишка проигнорирует
    )
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(
            text=get_text("doctor_menu_button", user_language),
            callback_data="doctor_menu")],
    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        get_text("patient_drop_success_message", lang=user_language).format(patient['name']),
        reply_markup=inline_keyboard)


@doctor_router.callback_query(DoctorsPatientChoose.action and F.data == "get_patient_medical_card")
async def get_patient_medical_card(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    patient_id = (await state.get_data())["patient_id"]

    file = URLInputFile(
        await get_user_diseases_url(user_id=patient_id,
                                    period_for_load=-1,  # -1 потому что всегда получаем полную карточку
                                    user_language=user_language,
                                    response_format="docx"),
        filename=get_text("diseases_filename", user_language)
    )
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text=get_text("back_to_patient_menu_button", user_language),
                              callback_data=f"{patient_id}")],
        [InlineKeyboardButton(text=get_text("doctor_menu_button", user_language),
                              callback_data="doctor_menu")]
    ])
    await state.set_state(DoctorsPatientChoose.patient_id)
    await callback.message.delete()

    await callback.message.answer_document(caption=get_text("get_patient_medical_card_message", user_language),
                                           document=file)
    await callback.message.answer(get_text("what_is_next", user_language),
                                  reply_markup=inline_keyboard)


@doctor_router.callback_query(DoctorsPatientChoose.action and F.data == "add_disease_for_patient")
async def doctor_choose_patient_id_handler(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']

    await callback.message.answer(get_text("add_disease_message", user_language))
    patient_id = (await state.get_data())["patient_id"]
    await state.clear()

    await state.set_state(DiseaseAdd.title)
    await state.update_data(for_patient=patient_id)


@doctor_router.callback_query(DoctorsPatientChoose.action and F.data == "add_appointment_for_patient")
async def appointment_add_handler(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    patient_id = (await state.get_data())["patient_id"]
    await state.clear()
    await callback.message.edit_text(get_text("appointment_date_message", user_language))
    await state.set_state(DoctorAddAppointment.date)
    await state.update_data(patient_id=patient_id)


@doctor_router.message(DoctorAddAppointment.date)
async def appointment_date_handler(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    date = message.text.lower()
    if not re.fullmatch(DATE_REGEX, date):
        await message.answer(text=get_text("incorrect_date_message", lang=user_language))
        return
    await state.update_data(date=date)
    await message.answer(get_text("appointment_time_message", user_language))
    await state.set_state(DoctorAddAppointment.time)


@doctor_router.message(DoctorAddAppointment.time)
async def appointment_time_handler(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    time = message.text.lower()
    if not re.match(TIME_REGEX, time):
        await message.answer(get_text("time_format_error", user_language))
        return
    await state.update_data(time=time)
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=get_text("yes", user_language),
                              callback_data="yes_button")
         ],
        [InlineKeyboardButton(text=get_text("no", user_language),
                              callback_data="no_button")
         ],
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(get_text("appointment_notify_your_self_message", user_language),
                         reply_markup=inline_keyboard)
    await state.set_state(DoctorAddAppointment.notify_your_self)


@doctor_router.callback_query(DoctorAddAppointment.notify_your_self)
async def appointment_self_notify_handler(callback: CallbackQuery, state: FSMContext):
    doctor = await get_user_by_id(callback.message.chat.id)
    user_language: str = doctor['language']
    if callback.data.startswith("yes"):
        await state.update_data(notify_your_self=True)
    else:
        await state.update_data(notify_your_self=False)
    notification_data = await state.get_data()
    patient = await get_user_by_id(notification_data['patient_id'])

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text=get_text("back_to_patient_menu_button", user_language),
                              callback_data=f"{notification_data['patient_id']}")],
        [InlineKeyboardButton(text=get_text("doctor_menu_button", user_language),
                              callback_data="doctor_menu")]
    ])
    await state.set_state(DoctorsPatientChoose.patient_id)
    notifications = await schedule_doctor_visit(doctor, patient, notification_data)
    try:
        for notification_data_piece in notifications:
            await add_notification(notification_data_piece)

    except Exception as x:
        logging.error(x)
        await callback.message.answer(get_text("notifications_add_error", user_language).format(x),
                                      reply_markup=inline_keyboard)
        await state.clear()
        return
    await schedule_notifications(bot=callback.message.bot,
                                 data=notifications)
    await callback.message.edit_text(get_text("appointment_add_success_message", user_language),
                                     reply_markup=inline_keyboard)
