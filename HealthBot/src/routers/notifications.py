import datetime
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove, URLInputFile

from src.scheduler.main import scheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

notification_router = Router()


async def send_notification(bot: Bot,
                            user_id: int,
                            message_text='test_message'):
    await bot.send_message(chat_id=user_id, text=message_text)


async def schedule_notification(bot: Bot,
                                user_id: int,
                                end_date: datetime.datetime,
                                message_text: str = None):
    scheduler.add_job(
        func=send_notification,
        kwargs={"bot": bot,
                "user_id": user_id,
                "message_text": message_text
                },
        trigger=CronTrigger(minute="*"),  # Время выполнения: 12:00, 16:00, 20:00
        end_date=end_date
    )


async def schedule_notifications(bot: Bot,
                                 data: list[dict]) -> list[str]:
    outdated_notifications = []
    for notification_data in data:
        if notification_data['end_date'] < datetime.datetime.now():
            outdated_notifications.append(notification_data['id'])
            continue
        await schedule_notification(bot,
                                    user_id=notification_data['user_id'],
                                    end_date=notification_data['end_date'],
                                    message_text=notification_data['message_text'])

    return outdated_notifications


@notification_router.callback_query(F.data == "make_notification")
async def make_notification(callback: CallbackQuery):
    end_date = datetime.datetime.now() + datetime.timedelta(days=1)
    # scheduler.ctx.add_instance(callback.message.bot, declared_class=Bot)

    # await send_notification(callback.message.bot,
    #                         callback.message.chat.id)
