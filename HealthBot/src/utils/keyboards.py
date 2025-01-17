from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.localizations import get_text


def generate_reply_keyboard(labels_for_buttons: list[str],
                            inline_tip: str,
                            row_size: int) -> ReplyKeyboardMarkup:
    buttons = []
    button_row = []
    for label in labels_for_buttons:
        button_row.append(KeyboardButton(text=label))
        if len(button_row) == row_size:
            buttons.append(button_row)
            button_row = []
    if button_row:
        buttons.append(button_row)
    keyboard = ReplyKeyboardMarkup(keyboard=buttons,
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder=inline_tip)

    return keyboard


def generate_days_keyboard(user_language: str) -> ReplyKeyboardMarkup:
    labels = [
        get_text("disease_today_date_word", lang=user_language),
        get_text("disease_yesterday_date_word", lang=user_language)
    ]
    keyboard = generate_reply_keyboard(labels_for_buttons=labels,
                                       inline_tip=get_text("disease_date_choose_inline_tip", user_language),
                                       row_size=len(labels))
    return keyboard
