import datetime
import logging
import re

from aiogram import Router, F, Bot
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext

from src.localizations import get_text
from src.api.handlers import get_user_by_id, add_notification, get_user_notifications, delete_notification
from src.states.notification_medicine_add import MedicineNotificationAdd
from src.constants import DEFAULT_NOTIFICATIONS_DURATION_ROW_SIZE, DEFAULT_NOTIFICATIONS_TIMES_A_DAY_ROW_SIZE
from src.utils.keyboards import generate_reply_keyboard
from src.utils.regex import TIME_REGEX
from src.utils.message_formatters import generate_notifications_message
from src.utils.timezone import MSK
from src.scheduler.utils import schedule_notifications

notification_router = Router()


@notification_router.callback_query(F.data == "make_notification")
async def notification_menu(callback: CallbackQuery):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']

    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(
            text=get_text("notifications_get_all_button", user_language),
            callback_data="get_all_notifications")],
        [InlineKeyboardButton(
            text=get_text("make_medicine_notification_button", user_language),
            callback_data="make_medicine_notification")],
        # [InlineKeyboardButton(
        #     text=get_text("make_doctor_notification_button", user_language),
        #     callback_data="make_doctor_notification")],
        [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                              callback_data="to_main_menu")]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(get_text("notifications_main_menu_message", user_language),
                                     reply_markup=inline_keyboard)


@notification_router.callback_query(F.data == "get_all_notifications")
async def get_all_notifications(callback: CallbackQuery):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    notifications = await get_user_notifications(user_id=callback.message.chat.id)
    buttons: list[list[InlineKeyboardButton]] = []
    if notifications:
        buttons.append([InlineKeyboardButton(text=get_text("notifications_delete_button", user_language),
                                             callback_data="notifications_delete_button")])
    buttons.append([InlineKeyboardButton(text=get_text("back_button", user_language),
                                         callback_data="back_notifications_menu")])
    buttons.append([InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                                         callback_data="to_main_menu")])
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(text=generate_notifications_message(notifications, user_language),
                                     reply_markup=inline_keyboard)


@notification_router.callback_query(F.data == "notifications_delete_button")
async def notifications_delete(callback: CallbackQuery):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    buttons = [
        [InlineKeyboardButton(text=get_text("back_button", user_language),
                              callback_data="back_notifications_delete")],
    ]

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        notifications = await get_user_notifications(user_id=callback.message.chat.id)
    except Exception as x:
        logging.error(f"Ошибка получения уведомлений : {x}")
        await callback.message.answer(text=get_text("unexpected_error", user_language).format(x),
                                      reply_markup=inline_keyboard)
        return
    for i, notification in enumerate(notifications):
        button = [InlineKeyboardButton(text=f"№{i + 1} {notification['message'].split(':')[1]}",
                                       callback_data=f"notification_id_{notification['id']}")]
        buttons.insert(i, button)

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        get_text("notifications_choose_to_delete", user_language) +
        generate_notifications_message(notifications,
                                       user_language),
        reply_markup=inline_keyboard)


@notification_router.callback_query(F.data.startswith("notification_id"))
async def delete_notification_handler(callback: CallbackQuery):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']

    notification_id = int(callback.data.split("_")[-1])
    buttons = [
        [InlineKeyboardButton(text=get_text("back_button", user_language),
                              callback_data="back_notification_deleted")],
        [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                              callback_data="to_main_menu")],
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await delete_notification(notification_id)
    except Exception as x:
        logging.error(f"Ошибка завершения болезни: {x}")
        await callback.message.answer(text=get_text("unexpected_error", user_language).format(x),
                                      reply_markup=inline_keyboard)
        return

    await callback.message.edit_text(get_text("notification_deleted_message", user_language),
                                     reply_markup=inline_keyboard)


@notification_router.callback_query(F.data == "make_medicine_notification")
async def make_medicine_notification(callback: CallbackQuery, state: FSMContext):
    user_language: str = (await get_user_by_id(callback.message.chat.id))['language']
    await state.set_state(MedicineNotificationAdd.medicine_name)
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                              callback_data="to_main_menu")]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(get_text("notifications_chose_medicine_message", user_language),
                                     reply_markup=inline_keyboard)


@notification_router.message(MedicineNotificationAdd.medicine_name)
async def choose_time_to_notify(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']

    await state.update_data(medicine_name=message.text)
    await state.set_state(MedicineNotificationAdd.duration)

    keyboard = generate_reply_keyboard(
        labels_for_buttons=get_text("notifications_default_duration_list", user_language),
        inline_tip=get_text("notifications_duration_inline_tip", user_language),
        row_size=DEFAULT_NOTIFICATIONS_DURATION_ROW_SIZE)

    await message.answer(get_text("notifications_duration_message", user_language) +
                         get_text("notifications_duration_inline_tip", user_language),
                         reply_markup=keyboard)


@notification_router.message(MedicineNotificationAdd.duration)
async def chose_how_many_times(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    if not message.text.isdigit():
        await message.answer(get_text("notifications_duration_type_error", user_language))
        return

    await state.update_data(duration=int(message.text))
    await state.set_state(MedicineNotificationAdd.times_a_day)

    keyboard = generate_reply_keyboard(
        labels_for_buttons=get_text("notifications_times_a_day_list", user_language),
        inline_tip=get_text("notifications_times_a_day_inline_tip", user_language),
        row_size=DEFAULT_NOTIFICATIONS_TIMES_A_DAY_ROW_SIZE
    )

    await message.answer(get_text("notifications_times_a_day_message", user_language),
                         reply_markup=keyboard)


@notification_router.message(MedicineNotificationAdd.times_a_day)
async def choose_time(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    if not message.text.isdigit():
        await message.answer(get_text("notifications_times_a_day_type_error", user_language))
        return
    if not int(message.text) > 0:
        await message.answer(get_text("notifications_times_a_day_validation_error", user_language))
        return

    await state.update_data(times_a_day=int(message.text))
    await state.set_state(MedicineNotificationAdd.time_notifications)
    await message.answer(get_text("time_format_error", user_language) + "\n" +
                         get_text("notifications_time_increase_error", user_language))
    # тут в сообщении ниже константная единица из-за того что всегда отсюда мы придем за первым временем приема
    await message.answer(get_text("notifications_choose_time_message", user_language).format("1"))


@notification_router.message(MedicineNotificationAdd.time_notifications)
async def choose_notification_times(message: Message, state: FSMContext):
    user_language: str = (await get_user_by_id(message.chat.id))['language']
    if not re.match(TIME_REGEX, message.text):
        await message.answer(get_text("time_format_error", user_language))
        return
    new_time_str = message.text
    new_time = tuple(map(int, new_time_str.split(":")))
    if times := await state.get_value("time_notifications"):
        if tuple(map(int, times[-1]['time'].split(":"))) >= new_time:
            await message.answer(get_text("notifications_time_increase_error", user_language))
            return
        times.append({"time": new_time_str})
    else:
        times = [{"time": new_time_str}]

    await state.update_data(time_notifications=times)

    times_a_day = await state.get_value("times_a_day")

    if times_a_day == len(times):
        # мы получили все times_a_day времен и можем сохранять нотификацию
        data = await state.get_data()
        times_string = ", ".join([f"{t['time']}" for t in times])
        buttons: list[list[InlineKeyboardButton]] = [
            [InlineKeyboardButton(text=get_text("to_main_menu_button", user_language),
                                  callback_data="to_main_menu")]
        ]
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        data['user_id'] = message.chat.id
        data.pop('times_a_day')
        data["end_date"] = datetime.datetime.now(MSK) + datetime.timedelta(days=data.pop("duration"))
        medicine_name = data.pop('medicine_name')
        data['message'] = get_text("notifications_message", user_language).format(medicine_name)
        try:
            logging.info(f"Добавлено уведомление {data}")
            await add_notification(data)
        except Exception as x:
            logging.error(x)
            await message.answer(get_text("notifications_add_error", user_language).format(x))
            await state.clear()
            return
        await schedule_notifications(bot=message.bot,
                                     data=[data])
        await message.answer(
            get_text("notifications_add_successful_message", user_language).format(
                medicine_name=medicine_name,
                duration=data['end_date'].strftime("%m-%d-%Y, %H:%M:%S"),
                times=times_string),
            reply_markup=inline_keyboard
        )
        await state.clear()
        return

    await message.answer(get_text("notifications_choose_time_message", user_language).format(str(len(times) + 1)))
