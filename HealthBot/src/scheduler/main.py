import datetime
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def start_up(bot):
    from src.routers.notifications import schedule_notifications
    from src.api.handlers import get_all_notifications, delete_notification
    scheduler.start()
    # load tasks from api
    notifications = await get_all_notifications()
    for notification in notifications:
        notification['end_date'] = datetime.datetime.fromisoformat(notification['end_date']).strftime("%d.%m.%Y")
    outdated_notifications_ids = await schedule_notifications(bot, notifications)
    for id in outdated_notifications_ids:
        try:
            await delete_notification(notification_id=int(id))
        except Exception as x:
            logging.error(f"Ошибка удаления уведомления {id}: {x}")
