import logging
import re

from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from src.api.handlers import get_user_by_id, add_disease, get_user_diseases
from src.localizations.main import get_text, AVAILABLE_LANGS, DEFAULT_LANG
from src.states.disease_add import DiseaseAdd
from src.utils.regex import DATE_REGEX
from .main_menu import send_main_menu

disease_router = Router()


@disease_router.callback_query(F.data == "add_disease")
async def change_info(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    # TODO: добавить список дефолтных болезней
    # common_diseases_
    # inline_keyboard: list[list[InlineKeyboardButton]] = [
    #     [InlineKeyboardButton(text=get_text("ARVI", user_language),
    #                           callback_data="name_field")],
    #     [InlineKeyboardButton(text=get_text("gender_field", user_language),
    #                           callback_data="gender_field")],
    #     [InlineKeyboardButton(text=get_text("weight_field", user_language),
    #                           callback_data="weight_field")],
    #     [InlineKeyboardButton(text=get_text("height_field", user_language),
    #                           callback_data="height_field")],
    #     [InlineKeyboardButton(text=get_text("language_field", user_language),
    #                           callback_data="language_field")],
    #     [InlineKeyboardButton(text=get_text("back_button", user_language),
    #                           callback_data="back_check_info")], ]

    await callback.message.edit_text(get_text("add_disease_message", user_language))  # , reply_markup=inline_keyboard)

    await state.set_state(DiseaseAdd.title)


@disease_router.message(DiseaseAdd.title)
async def title_chosen(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']

    await state.update_data(title=message.text)
    await message.answer(text=get_text("disease_description_message", lang=user_language))
    await state.set_state(DiseaseAdd.description)


@disease_router.message(DiseaseAdd.description)
async def description_chosen(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    await state.update_data(description=message.text)
    await message.answer(text=get_text("disease_date_start_message", lang=user_language))
    await state.set_state(DiseaseAdd.date_from)


@disease_router.message(DiseaseAdd.date_from)
async def date_from_chosen(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    date_from = message.text
    if not re.fullmatch(DATE_REGEX, date_from):
        await message.answer(text=get_text("disease_incorrect_date", lang=user_language))
        return
    await state.update_data(date_from=date_from)

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
            logging.error("fsdfsd")
            await message.answer(text=get_text("disease_add_success_message", lang=user_language),
                                 reply_markup=inline_keyboard)
    else:
        await message.answer(text=get_text("disease_add_success_message", lang=user_language),
                             reply_markup=inline_keyboard)
    data = await state.get_data()
    data['user_id'] = message.chat.id
    await add_disease(data)

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
    await disease_add_end(user_language, message, state, edit=False)


@disease_router.callback_query(F.data == "get_diseases")
async def change_info(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    diseases = await get_user_diseases(callback.message.chat.id)
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                              callback_data="to_main_menu")]
    ])
    await callback.message.edit_text(
        get_text("get_diseases_message", user_language).format(diseases), reply_markup=inline_keyboard)
