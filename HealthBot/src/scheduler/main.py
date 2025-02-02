import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.api.handlers import get_all_notifications

scheduler = AsyncIOScheduler()


async def start_up(bot):
    from src.scheduler.utils import schedule_notifications, delete_notifications, schedule_notification_cleanup

    scheduler.start()
    notifications = await get_all_notifications()
    outdated_notifications_ids = await schedule_notifications(bot, notifications)
    await delete_notifications(outdated_notifications_ids)

    await schedule_notification_cleanup()
