from aiogram.types import ReplyKeyboardRemove


async def remove_chat_buttons(message,
                              msg_text: str = r"."):
    """Deletes buttons below the chat.
    For now there are no way to delete kbd other than inline one, check
        https://core.telegram.org/bots/api#updating-messages.
    """
    msg = await message.answer(msg_text,
                                 reply_markup=ReplyKeyboardRemove())
    await msg.delete()
