from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, F

from src.states.user_registration import UserRegistration
from src.states.user_change_data import UserChangeData
from src.constants import MAX_HEIGHT_AND_WEIGHT
from src.api.handlers import add_user, get_user_by_id, update_user, get_user_active_diseases
from src.localizations import get_text, AVAILABLE_LANGS, DEFAULT_LANG
from src.routers.main_menu import send_main_menu

user_router = Router()


@user_router.callback_query(UserRegistration.language)
async def language_chosen(callback: CallbackQuery, state: FSMContext):
    await state.update_data(language=callback.data)
    await callback.message.edit_text(text=get_text("name_message", lang=callback.data))
    await state.set_state(UserRegistration.name)


@user_router.message(UserRegistration.name)
async def name_chosen(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_language: str = (await state.get_data())['language']
    genders: list = get_text("gender_list", user_language)
    buttons: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text=gender, callback_data=gender)] for gender in
                                                 genders]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text=get_text("gender_message", lang=user_language),
                         reply_markup=inline_keyboard)
    await state.set_state(UserRegistration.gender)


@user_router.callback_query(UserRegistration.gender)
async def gender_chosen(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    await callback.message.edit_text(text=get_text("weight_message", lang=(await state.get_data())['language']))
    await state.set_state(UserRegistration.weight)


@user_router.message(UserRegistration.weight)
async def weight_chosen(message: Message, state: FSMContext):
    user_language: str = (await state.get_data())['language']
    if not message.text.isdigit():
        await message.answer(text=get_text("weight_error_message", lang=user_language))
        return
    elif int(message.text) > MAX_HEIGHT_AND_WEIGHT:
        await message.answer(text=get_text("weight_overflow_error_message",
                                           lang=user_language).format(MAX_HEIGHT_AND_WEIGHT))
        return
    await state.update_data(weight=int(message.text))
    await message.answer(text=get_text("height_message", lang=user_language))
    await state.set_state(UserRegistration.height)


@user_router.message(UserRegistration.height)
async def height_chosen(message: Message, state: FSMContext):
    user_language: str = (await state.get_data())['language']
    if not message.text.isdigit():
        await message.answer(text=get_text("height_error_message", lang=user_language))
        return
    elif int(message.text) > MAX_HEIGHT_AND_WEIGHT:
        await message.answer(text=get_text("height_overflow_error_message", lang=user_language).format(
            MAX_HEIGHT_AND_WEIGHT))
        return
    await state.update_data(height=int(message.text))
    await message.answer(
        text=get_text("register_complete_message", lang=(await state.get_data())['language']))
    user_data: dict = await state.get_data()
    user_data['id'] = int(message.chat.id)
    await add_user(user_data)
    await state.clear()
    await send_main_menu(message)


@user_router.callback_query(F.data == "change_info")
async def change_info(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']

    buttons: list[list[InlineKeyboardButton]] = []
    fields = ['name', 'gender', 'language', 'weight', 'height']  # FIXME:
    for field in fields:
        buttons.append(
            [InlineKeyboardButton(text=get_text(field + "_field", user_language),
                                  callback_data=field + "_field")])
    buttons.append([InlineKeyboardButton(text=get_text("back_button", user_language), callback_data="back_check_info")])
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await state.set_state(UserChangeData.field_name)
    await callback.message.edit_text(get_text("change_info_message", user_language), reply_markup=inline_keyboard)


@user_router.callback_query(F.data == "check_personal_data")
async def get_info(callback: CallbackQuery):
    user_info: dict = await get_user_by_id(callback.message.chat.id)
    user_language: str = user_info['language']

    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=get_text("change_data_message", user_language),
                              callback_data="change_info")],
        [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                              callback_data="to_main_menu")]
    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    user_info['language'] = AVAILABLE_LANGS.get(user_info['language'], user_info['language'])
    diseases: str = ", ".join([disease['title'] for disease in
                               (await get_user_active_diseases(callback.message.chat.id))])
    additional_message = get_text("user_info_current_status_message", user_language)
    if diseases:
        additional_message = get_text("user_info_current_diseases_message", user_language).format(diseases=diseases)

    await callback.message.edit_text(
        get_text("user_info_message", user_language).format(**user_info) + additional_message,
        reply_markup=inline_keyboard)


@user_router.callback_query(UserChangeData.field_name)
async def change_piece(callback: CallbackQuery, state: FSMContext):
    field_name = callback.data.split('_')[0]
    await state.update_data(field_name=field_name)
    user_language = (await get_user_by_id(callback.message.chat.id))['language']
    if field_name == "gender":
        genders: list = get_text("gender_list", user_language)
        buttons: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text=gender, callback_data=gender)] for
                                                     gender in
                                                     genders]

        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.edit_text(text=get_text("gender_message", lang=user_language),
                                         reply_markup=inline_keyboard)
    elif field_name == "language":
        inline_keyboard = [[]]
        for callback_, text in AVAILABLE_LANGS.items():
            inline_keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_)])
        await callback.message.edit_text(text=get_text('language_message', user_language),
                                      reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
    else:
        await callback.message.edit_text(
            text=get_text("enter_new_data_for_change_message", lang=user_language).format(
                get_text(callback.data, lang=user_language))
        )
    await state.set_state(UserChangeData.new_data)


@user_router.callback_query(UserChangeData.new_data)
async def change_data_callback_handler(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    await state.update_data(new_data=callback.data)
    data: dict = await state.get_data()
    try:
        await update_user(callback.message.chat.id, data['field_name'], data['new_data'])
    except Exception as x:
        await callback.message.edit_text(text=get_text("unexpected_error", user_language).format(x))
        return

    await state.clear()

    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']

    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=get_text("back_button", user_language),
                              callback_data="back_check_info")],
        [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                              callback_data="to_main_menu")]
    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text=get_text("user_change_data_success_message", user_language),
                                     reply_markup=inline_keyboard)


@user_router.message(UserChangeData.new_data)
async def change_data_message_handler(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    field_name = await state.get_value('field_name')
    message_text = message.text
    if field_name in ("gender", "language"):
        await message.answer(text=get_text("only_button_input_allowed_message", lang=user_language))
        return
    elif field_name == "weight":
        if not message_text.isdigit():
            await message.answer(text=get_text("weight_error_message", lang=user_language))
            return
        elif int(message_text) > MAX_HEIGHT_AND_WEIGHT:
            await message.answer(
                text=get_text("weight_overflow_error_message", lang=user_language).format(MAX_HEIGHT_AND_WEIGHT))
            return
        message_text = int(message_text)
    elif field_name == "height":
        if not message_text.isdigit():
            await message.answer(text=get_text("height_error_message", lang=user_language))
            return
        elif int(message_text) > MAX_HEIGHT_AND_WEIGHT:
            await message.answer(
                text=get_text("height_overflow_error_message", lang=user_language).format(MAX_HEIGHT_AND_WEIGHT))
            return
        message_text = int(message_text)

    await state.update_data(new_data=message_text)
    data: dict = await state.get_data()
    try:
        await update_user(message.chat.id, data['field_name'], data['new_data'])
    except Exception as x:
        await message.answer(text=get_text("unexpected_error", user_language).format(x))
        return

    await state.clear()

    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=get_text("back_button", user_language),
                              callback_data="back_check_info")],
        [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                              callback_data="to_main_menu")]
    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text=get_text("user_change_data_success_message", user_language),
                         reply_markup=inline_keyboard)


@user_router.message(StateFilter(None))
@user_router.message(Command("start"))
async def registration_start(message: Message, state: FSMContext):
    if user := (await get_user_by_id(message.chat.id)):
        await message.answer(
            text=get_text('greet_message', user['language']).format(user['name']))
        await send_main_menu(message)
    else:
        language: str = message.from_user.language_code if message.from_user.language_code in AVAILABLE_LANGS else DEFAULT_LANG
        inline_keyboard = [[]]
        for callback, text in AVAILABLE_LANGS.items():
            inline_keyboard.append([InlineKeyboardButton(text=text, callback_data=callback)])
        await message.answer(text=get_text('language_message', language),
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
        await state.set_state(UserRegistration.language)
