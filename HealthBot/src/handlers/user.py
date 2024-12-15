from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, F

from src.states.user_registration import UserRegistration
from src.states.user_change_data import UserChangeData
from src.api.handlers import add_user, get_user_by_id, update_user
from src.localizations.main import get_text, AVAILABLE_LANGS, DEFAULT_LANG
from .main_menu import send_main_menu

user_router = Router()


@user_router.callback_query(lambda call: call.data in AVAILABLE_LANGS.keys())
async def language_chosen(callback: CallbackQuery, state: FSMContext):
    await state.update_data(language=callback.data)
    await callback.message.edit_text(text=get_text("name_message", lang=callback.data))
    await state.set_state(UserRegistration.name)


@user_router.message(UserRegistration.name)
async def name_chosen(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=get_text("gender_message", lang=(await state.get_data())['language']))
    await state.set_state(UserRegistration.gender)


@user_router.message(UserRegistration.gender)
async def name_chosen(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer(text=get_text("weight_message", lang=(await state.get_data())['language']))
    await state.set_state(UserRegistration.weight)


@user_router.message(UserRegistration.weight)
async def name_chosen(message: Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    await message.answer(text=get_text("height_message", lang=(await state.get_data())['language']))
    await state.set_state(UserRegistration.height)


@user_router.message(UserRegistration.height)
async def gender_chosen(message: Message, state: FSMContext):
    await state.update_data(height=int(message.text))
    await message.answer(
        text=get_text("register_complete_message", lang=(await state.get_data())['language']))
    user_data: dict = await state.get_data()
    user_data['id'] = int(message.chat.id)
    await add_user(user_data)
    await state.clear()
    await send_main_menu(message)


@user_router.callback_query(F.data == "change_info")
async def change_info(callback: CallbackQuery):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    buttons: list[list[InlineKeyboardButton]] = [[InlineKeyboardButton(text=get_text("name_field", user_language),
                                                                       callback_data="name_field")],
                                                 [InlineKeyboardButton(text=get_text("gender_field", user_language),
                                                                       callback_data="gender_field")],
                                                 [InlineKeyboardButton(text=get_text("weight_field", user_language),
                                                                       callback_data="weight_field")],
                                                 [InlineKeyboardButton(text=get_text("height_field", user_language),
                                                                       callback_data="height_field")],
                                                 [InlineKeyboardButton(text=get_text("language_field", user_language),
                                                                       callback_data="language_field")],
                                                 [InlineKeyboardButton(text=get_text("back_button", user_language),
                                                                       callback_data="back_check_info")], ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

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
    await callback.message.edit_text(
        get_text("user_info_message", user_language).format(user_info['name'],
                                                            user_info['gender'],
                                                            user_info['language'],
                                                            user_info['weight'],
                                                            user_info['height'],
                                                            ), reply_markup=inline_keyboard)


@user_router.callback_query(F.data.contains("field"))
async def change_piece(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserChangeData.field_name)
    await state.update_data(field_name=callback.data.split('_')[0])
    await state.set_state(UserChangeData.new_data)
    user_lang = (await get_user_by_id(callback.message.chat.id))['language']
    await callback.message.answer(
        text=get_text("enter_new_data_for_change_message", lang=user_lang).format(get_text(callback.data, lang=user_lang))
    )


@user_router.message(UserChangeData.new_data)
async def change_data(message: Message, state: FSMContext):
    await state.update_data(new_data=message.text)
    data: dict = await state.get_data()
    await update_user(message.chat.id, data['field_name'], data['new_data'])
    await state.clear()
    await send_main_menu(message)


@user_router.message(StateFilter(None), Command("start"))
@user_router.message()
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
