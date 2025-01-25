import logging
import re

from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    ReplyKeyboardRemove,
    URLInputFile
)
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from src.api.handlers import (
    get_user_by_id,
    add_disease,
    get_user_diseases,
    get_user_diseases_url,
    get_user_active_diseases,
    finish_disease,
    get_disease,
)
from src.localizations import get_text
from src.states.disease_add import DiseaseAdd
from src.states.disease_request import DiseaseRequest
from src.utils.regex import DATE_REGEX
from src.utils.message_formatters import generate_diseases_message, generate_active_diseases_message
from src.utils.chat_keyboard_clearer import remove_chat_buttons
from src.utils.keyboards import generate_days_keyboard, generate_reply_keyboard
from src.utils.date_checker import check_message_for_date
from src.constants import DEFAULT_DISEASES_LIST_ROW_SIZE

disease_router = Router()


@disease_router.callback_query(F.data == "add_disease")
async def add_disease_handler(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    keyboard = generate_reply_keyboard(
        labels_for_buttons=get_text("default_diseases_list", user_language),
        inline_tip=get_text("disease_choose_inline_tip", user_language),
        row_size=DEFAULT_DISEASES_LIST_ROW_SIZE
    )

    await callback.message.answer(get_text("add_disease_message", user_language), reply_markup=keyboard)

    await state.set_state(DiseaseAdd.title)


@disease_router.message(DiseaseAdd.title)
async def title_chosen(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']

    await state.update_data(title=message.text)
    await message.answer(text=get_text("disease_description_message", lang=user_language),
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(DiseaseAdd.description)


@disease_router.message(DiseaseAdd.description)
async def description_chosen(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    await state.update_data(description=message.text)
    await message.answer(text=get_text("disease_treatment_plan_message", lang=user_language))
    await state.set_state(DiseaseAdd.treatment_plan)


@disease_router.message(DiseaseAdd.treatment_plan)
async def treatment_plan_chosen(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    await state.update_data(treatment_plan=message.text)
    keyboard = generate_days_keyboard(user_language)
    await message.answer(text=get_text("disease_date_start_message", lang=user_language), reply_markup=keyboard)
    await state.set_state(DiseaseAdd.date_from)


@disease_router.message(DiseaseAdd.date_from)
async def date_from_chosen(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    date_from = message.text.lower()
    if date_candidate := check_message_for_date(date_from, user_language):
        date_from = date_candidate
    elif not re.fullmatch(DATE_REGEX, date_from):
        await message.answer(text=get_text("disease_incorrect_date", lang=user_language))
        return
    await state.update_data(date_from=date_from)
    await remove_chat_buttons(message, user_language)
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=get_text("yes", user_language),
                              callback_data="yes_button")
         ],
        [InlineKeyboardButton(text=get_text("no", user_language),
                              callback_data="no_button")
         ],
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text=get_text("disease_still_sick_message", lang=user_language),
                         reply_markup=inline_keyboard)
    await state.set_state(DiseaseAdd.still_sick)


async def disease_add_end(user_language,
                          message,
                          state,
                          edit=False):
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(
            text=get_text("make_medicine_notification_button", user_language),
            callback_data="make_medicine_notification")],
        [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                              callback_data="to_main_menu")]
    ])
    data = await state.get_data()
    data['user_id'] = message.chat.id

    try:
        await add_disease(data)
    except Exception as x:
        await message.answer(text=get_text("unexpected_error", user_language).format(x), reply_markup=inline_keyboard)
        return
    if edit:
        try:
            await message.edit_text(text=get_text("disease_add_success_message", lang=user_language),
                                    reply_markup=inline_keyboard)
        except Exception:
            await message.answer(text=get_text("disease_add_success_message", lang=user_language),
                                 reply_markup=inline_keyboard)
    else:
        await message.answer(text=get_text("disease_add_success_message", lang=user_language),
                             reply_markup=inline_keyboard)

    await state.clear()


@disease_router.callback_query(DiseaseAdd.still_sick)
async def still_sick_chosen(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    if callback.data.startswith("yes"):
        await state.update_data(still_sick=True)
        await disease_add_end(user_language, callback.message, state, edit=True)

    else:
        await state.update_data(still_sick=False)
        keyboard = generate_days_keyboard(user_language)
        await callback.message.answer(text=get_text("disease_date_end_message", lang=user_language),
                                      reply_markup=keyboard)
        await state.set_state(DiseaseAdd.date_to)


@disease_router.message(DiseaseAdd.date_to)
async def date_to_chosen(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    date_to = message.text.lower()
    if date_candidate := check_message_for_date(date_to, user_language):
        date_to = date_candidate
    elif not re.fullmatch(DATE_REGEX, date_to):
        await message.answer(text=get_text("disease_incorrect_date", lang=user_language))
        return
    await remove_chat_buttons(message, user_language)
    await state.update_data(date_to=date_to)
    await disease_add_end(user_language, message, state)


@disease_router.callback_query(F.data == "get_diseases")
async def diseases_time_menu(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    buttons = []
    button_row = []
    for label, duration in get_text("diseases_list_of_periods", user_language):
        button_row.append(InlineKeyboardButton(text=label,
                                               callback_data=f"period_{duration}"))
        if len(button_row) == DEFAULT_DISEASES_LIST_ROW_SIZE:
            buttons.append(button_row)
            button_row = []
    if button_row:
        buttons.append(button_row)
    buttons.append(
        [InlineKeyboardButton(text=get_text("back_button", user_language), callback_data="back_diseases_menu")])
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await state.set_state(DiseaseRequest.how_long)
    await callback.message.edit_text(get_text("choose_diseases_periods_message", user_language),
                                     reply_markup=inline_keyboard)


@disease_router.callback_query(DiseaseRequest.how_long)
async def diseases_type_menu(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    await state.update_data(how_long=int(callback.data.split("_")[1]))
    buttons = [[InlineKeyboardButton(text=piece[0],
                                     callback_data=piece[1])] for piece in
               get_text("diseases_list_message_type", user_language)]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(get_text("diseases_choose_how_to_get_message", user_language),
                                     reply_markup=inline_keyboard)
    await state.set_state(DiseaseRequest.how)


@disease_router.callback_query(DiseaseRequest.how)
async def get_diseases(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    period_for_load: int = (await state.get_data())['how_long']

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                              callback_data="to_main_menu")]
    ])

    try:
        diseases = await get_user_diseases(callback.message.chat.id, period_for_load)
    except Exception as x:
        logging.debug(f"Ошибка получения болезней за {period_for_load} c помощью {callback.data}: {x}")
        await callback.message.answer(text=get_text("unexpected_error", user_language).format(x),
                                      reply_markup=inline_keyboard)
        return

    if not diseases:
        await callback.message.edit_text(
            get_text("get_diseases_empty_message", user_language),
            reply_markup=inline_keyboard)

    elif callback.data == "telegram":
        await callback.message.edit_text(
            get_text("get_diseases_message", user_language) + generate_diseases_message(diseases, user_language),
            reply_markup=inline_keyboard)
    elif callback.data == "word":
        file = URLInputFile(
            await get_user_diseases_url(user_id=callback.message.chat.id,
                                        period_for_load=period_for_load,
                                        user_language=user_language,
                                        response_format="docx"),
            filename=get_text("diseases_filename", user_language)
        )
        await callback.message.delete()

        await callback.message.answer_document(caption=get_text("get_diseases_message", user_language),
                                               document=file)
        await callback.message.answer(get_text("what_is_next", user_language),
                                      reply_markup=inline_keyboard)
    elif callback.data == "html":
        url = await get_user_diseases_url(user_id=callback.message.chat.id,
                                          period_for_load=period_for_load,
                                          user_language=user_language,
                                          response_format="html")
        await callback.message.edit_text(f'<a href="{url}">'
                                         f'{get_text("diseases_page_message", user_language)}</a>',
                                         reply_markup=inline_keyboard)
    else:
        await callback.message.edit_text(
            get_text("not_supported_message", user_language),
            reply_markup=inline_keyboard)

    await state.clear()


@disease_router.callback_query(F.data == "get_active_diseases")
async def get_active_diseases(callback: CallbackQuery):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']

    buttons = [

        [InlineKeyboardButton(text=get_text("back_button", user_language),
                              callback_data="back_diseases_menu")],

    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        diseases = await get_user_active_diseases(callback.message.chat.id)
    except Exception as x:
        logging.error(f"Ошибка получения активных болезней: {x}")
        await callback.message.answer(text=get_text("unexpected_error", user_language).format(x),
                                      reply_markup=inline_keyboard)
        return
    if diseases:
        buttons.insert(0, [InlineKeyboardButton(text=get_text("mark_disease_as_finished", user_language),
                                                callback_data="mark_disease_as_finished")])
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        get_text("get_active_diseases_message", user_language) + generate_diseases_message(diseases, user_language),
        reply_markup=inline_keyboard)


@disease_router.callback_query(F.data == "mark_disease_as_finished")
async def mark_disease_as_finished(callback: CallbackQuery):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']

    buttons = [

        [InlineKeyboardButton(text=get_text("back_button", user_language),
                              callback_data="back_diseases_mark")],

    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        diseases = await get_user_active_diseases(callback.message.chat.id)
    except Exception as x:
        logging.error(f"Ошибка получения активных болезней: {x}")
        await callback.message.answer(text=get_text("unexpected_error", user_language).format(x),
                                      reply_markup=inline_keyboard)
        return
    for i, disease in enumerate(diseases):
        button = [InlineKeyboardButton(text=f"№{i + 1} {disease['title']}",
                                       callback_data=f"disease_id_{disease['id']}")]
        buttons.insert(i, button)

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        get_text("diseases_choose_to_finish", user_language) + generate_active_diseases_message(diseases,
                                                                                                user_language),
        reply_markup=inline_keyboard)


@disease_router.callback_query(F.data.startswith("disease_id"))
async def mark_disease_as_finished(callback: CallbackQuery):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']

    disease_id = int(callback.data.split("_")[-1])
    buttons = [
        [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                              callback_data="to_main_menu")],
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
