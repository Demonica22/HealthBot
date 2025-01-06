from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.localizations import get_text


def generate_days_keyboard(user_language: str) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text=get_text("disease_today_date_word", lang=user_language)),
         KeyboardButton(text=get_text("disease_yesterday_date_word", lang=user_language))]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons,
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder=get_text("disease_date_choose_inline_tip", user_language))
    return keyboard
