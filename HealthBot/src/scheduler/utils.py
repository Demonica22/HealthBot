import logging
import datetime
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot

from src.localizations import get_text
from src.api.handlers import get_user_by_id, delete_notification, get_all_notifications
from src.scheduler.main import scheduler
from src.utils.timezone import MSK


async def send_notification(bot: Bot,
                            user_id: int,
                            message_text='test_message'):
    await bot.send_message(chat_id=user_id, text=message_text)


async def schedule_notification(bot: Bot,
                                user_id: int,
                                user_language: str,
                                end_date: datetime.datetime,
                                time: tuple[int],
                                medicine_name: str = None):
    message_text = get_text("notifications_message", user_language).format(medicine_name)
    logging.debug(f'Scheduled notification at {time} for {user_id}, end_date = {end_date}, with text = {message_text}')
    scheduler.add_job(
        func=send_notification,
        kwargs={
            "bot": bot,
            "user_id": user_id,
            "message_text": message_text
        },
        trigger=CronTrigger(hour=time[0], minute=time[1], end_date=end_date)
    )


async def filter_notifications(data: list[dict]) -> tuple[list[dict], list[str]]:
    outdated_notifications = []
    notifications_to_schedule = []
    for notification_data in data:
        notification_data['end_date'] = datetime.datetime.strptime(notification_data['end_date'], "%d.%m.%Y").replace(
            tzinfo=MSK)
        if notification_data['end_date'] < datetime.datetime.now(MSK):
            outdated_notifications.append(notification_data['id'])
        else:
            notifications_to_schedule.append(notification_data)

    return notifications_to_schedule, outdated_notifications


async def delete_notifications(data: list[str]):
    for notification_id in data:
        try:
            await delete_notification(notification_id=int(notification_id))
        except Exception as x:
            logging.error(f"Ошибка удаления уведомления {notification_id}: {x}")


async def schedule_notifications(bot: Bot,
                                 data: list[dict]) -> list[str]:
    notifications_to_schedule, outdated_notifications = await filter_notifications(data)
    for notification_data in notifications_to_schedule:
        user_language: str = (await get_user_by_id(notification_data['user_id']))['language']

        for time_data in notification_data['time_notifications']:
            time = tuple(map(int, time_data['time'].split(":")))
            await schedule_notification(bot,
                                        user_id=notification_data['user_id'],
                                        user_language=user_language,
                                        end_date=notification_data['end_date'],
                                        time=time,
                                        medicine_name=notification_data['medicine_name'])

    return outdated_notifications


async def notification_cleanup():
    notifications = await get_all_notifications()
    logging.info("Очищаю старые уведомления")
    for notification in notifications:
        notification['end_date'] = datetime.datetime.fromisoformat(notification['end_date']).strftime("%d.%m.%Y")
    _, outdated_notifications_ids = await filter_notifications(notifications)
    await delete_notifications(outdated_notifications_ids)


async def schedule_notification_cleanup():
    # тут 8 магическое число - наиболее странная минута для уведомлений
    # чтобы очистка уведомлений не задевала пользователей
    minute_to_delete_notifications = 8
    scheduler.add_job(
        func=notification_cleanup,
        trigger=CronTrigger(minute=minute_to_delete_notifications))
