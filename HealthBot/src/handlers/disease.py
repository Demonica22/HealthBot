import datetime
import logging
import re

from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from src.api.handlers import get_user_by_id, add_disease, get_user_diseases
from src.localizations.main import get_text, AVAILABLE_LANGS, DEFAULT_LANG
from src.states.disease_add import DiseaseAdd
from src.utils.regex import DATE_REGEX
from src.utils.message_formatters import generate_telegram_message
from src.utils.chat_keyboard_clearer import remove_chat_buttons

disease_router = Router()

default_diseases_list_row_size = 2


@disease_router.callback_query(F.data == "add_disease")
async def change_info(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    buttons = []
    button_row = []
    for label in get_text("default_diseases_list", user_language):
        button_row.append(KeyboardButton(text=label))

        if len(button_row) == default_diseases_list_row_size:
            buttons.append(button_row)
            button_row = []
    if button_row:
        buttons.append(button_row)
    keyboard = ReplyKeyboardMarkup(keyboard=buttons,
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder=get_text("disease_choose_inline_tip", user_language))
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
    buttons = [
        [KeyboardButton(text=get_text("disease_today_date_word", lang=user_language)),
         KeyboardButton(text=get_text("disease_yesterday_date_word", lang=user_language))]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons,
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder=get_text("disease_date_choose_inline_tip", user_language))
    await message.answer(text=get_text("disease_date_start_message", lang=user_language), reply_markup=keyboard)
    await state.set_state(DiseaseAdd.date_from)


@disease_router.message(DiseaseAdd.date_from)
async def date_from_chosen(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    date_from = message.text.lower()
    today = get_text("disease_today_date_word", lang=user_language).lower()
    yesterday = get_text("disease_yesterday_date_word", lang=user_language).lower()
    possible_word_dates = (today, yesterday)
    if date_from in possible_word_dates:
        if date_from == today:
            date_from = datetime.datetime.today().strftime("%d.%m.%Y")
        elif date_from == yesterday:
            date_from = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%d.%m.%Y")
    elif not re.fullmatch(DATE_REGEX, date_from):
        await message.answer(text=get_text("disease_incorrect_date", lang=user_language))
        return
    await state.update_data(date_from=date_from)
    await remove_chat_buttons(message)
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=get_text("yes_button", user_language),
                              callback_data="yes_button")
         ],
        [InlineKeyboardButton(text=get_text("no_button", user_language),
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
        [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                              callback_data="to_main_menu")]
    ])
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
    data = await state.get_data()
    data['user_id'] = message.chat.id
    try:
        await add_disease(data)
    except Exception as x:
        await message.answer(text=f"Непредвиденная ошибка: {x}", reply_markup=inline_keyboard)
    await state.clear()


@disease_router.callback_query(DiseaseAdd.still_sick)
async def description_chosen(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    if callback.data.startswith("yes"):
        await state.update_data(still_sick=True)
        await disease_add_end(user_language, callback.message, state, edit=True)

    else:
        await state.update_data(still_sick=False)
        await callback.message.edit_text(text=get_text("disease_date_end_message", lang=user_language))
        await state.set_state(DiseaseAdd.date_to)


@disease_router.message(DiseaseAdd.date_to)
async def date_to_chosen(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    date_to = message.text
    if not re.fullmatch(DATE_REGEX, date_to):
        await message.answer(text=get_text("disease_incorrect_date", lang=user_language))
        return
    await state.update_data(date_to=date_to)
    await disease_add_end(user_language, message, state)


@disease_router.callback_query(F.data == "get_diseases")
async def get_diseases(callback: CallbackQuery):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    diseases = await get_user_diseases(callback.message.chat.id)
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                              callback_data="to_main_menu")]
    ])
    await callback.message.edit_text(
        get_text("get_diseases_message", user_language).format(generate_telegram_message(diseases)),
        reply_markup=inline_keyboard)
