import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def start_up(bot):
    from src.routers.notifications import schedule_notifications
    scheduler.start()
    # load tasks from api
    tasks = []
    [{"id": 1,
      "end_date": datetime.datetime.now() + datetime.timedelta(days=1),
      "user_id": 438053520,
      "message_text": "Уведомление тестовое"
      }]
    outdated_notifications = await schedule_notifications(bot, tasks)
    # for task in tasks:
    #     scheduler.add_job(
    #         func=send_notification,
    #         kwargs={"bot": callback.message.bot,
    #                 "user_id": callback.message.chat.id},
    #         trigger=CronTrigger(minute="*"),  # Время выполнения: 12:00, 16:00, 20:00
    #         end_date=end_date,
    #         id="task_once"
    #     )
