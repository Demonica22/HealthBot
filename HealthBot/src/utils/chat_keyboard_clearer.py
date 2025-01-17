from aiogram.types import ReplyKeyboardRemove
from src.localizations import get_text


async def remove_chat_buttons(message,
                              user_language: str,
                              msg_text: str = None):
    """Deletes buttons below the chat.
    For now there are no way to delete kbd other than inline one, check
        https://core.telegram.org/bots/api#updating-messages.
    """
    if msg_text is None:
        msg_text = get_text("system_clear_keyboard", user_language)
    msg = await message.answer(msg_text,
                               reply_markup=ReplyKeyboardRemove(input_field_placeholder=None))
    await msg.delete()
