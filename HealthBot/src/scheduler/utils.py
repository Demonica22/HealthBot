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
                                end_date: datetime.datetime,
                                time: tuple[int, int],
                                start_date: datetime.datetime,
                                message: str = None):
    logging.debug(
        f'Scheduled notification at {time} for {user_id},start_date = {start_date}, '
        f'end_date = {end_date}, with text = {message}')

    scheduler.add_job(
        func=send_notification,
        kwargs={
            "bot": bot,
            "user_id": user_id,
            "message_text": message
        },
        trigger=CronTrigger(hour=time[0], minute=time[1], end_date=end_date, start_date=start_date)
    )


async def filter_notifications(data: list[dict]) -> tuple[list[dict], list[str]]:
    outdated_notifications = []
    notifications_to_schedule = []
    for notification_data in data:
        print(notification_data['end_date'], datetime.datetime.now(MSK))
        if notification_data['end_date'] < datetime.datetime.now(MSK):

            if 'id' in notification_data:
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
        for time_data in notification_data['time_notifications']:
            time = tuple(map(int, time_data['time'].split(":")))
            await schedule_notification(bot,
                                        user_id=notification_data['user_id'],
                                        end_date=notification_data['end_date'],
                                        time=time,
                                        start_date=notification_data.get('start_date', datetime.datetime.now(MSK)),
                                        message=notification_data['message'])

    return outdated_notifications


async def notification_cleanup():
    notifications = await get_all_notifications()
    logging.info("Очищаю старые уведомления")
    _, outdated_notifications_ids = await filter_notifications(notifications)
    await delete_notifications(outdated_notifications_ids)


async def schedule_notification_cleanup():
    # тут 8 магическое число - наиболее странная минута для уведомлений
    # чтобы очистка уведомлений не задевала пользователей
    minute_to_delete_notifications = 8
    scheduler.add_job(
        func=notification_cleanup,
        trigger=CronTrigger(minute=minute_to_delete_notifications))


async def schedule_doctor_visit(doctor: dict, patient: dict, notification_data: dict) -> list[dict]:
    one_hour_before = notification_data['time'].split(":")
    if one_hour_before[0] in ("00", "0"):
        one_hour_before = ["00", "00"]
    else:
        hour = str(int(one_hour_before[0]) - 1)
        if len(hour) == 1:
            hour = "0" + hour
        one_hour_before = [hour, one_hour_before[1]]
    one_hour_before = ":".join(one_hour_before)
    date = datetime.datetime.strptime(notification_data['date'], "%d.%m.%Y").replace(tzinfo=MSK)
    end_date = (datetime.datetime.strptime(notification_data['date'] + " " + notification_data['time'],
                                           "%d.%m.%Y %H:%M") + datetime.timedelta(hours=1)).replace(tzinfo=MSK)
    notifications = [
        # Уведомление за день до приема и в день приема (ровно во время приема)
        {
            'user_id': notification_data['patient_id'],
            'message': get_text("appointment_notification_for_patient_message", patient['language'])
            .format(doctor['name'],
                    notification_data['date'],
                    notification_data['time']),
            'end_date': end_date,
            'start_date': date - datetime.timedelta(days=1),
            'time_notifications': [{'time': notification_data['time']}]
        },
        # Уведомление за час до приема в дату приема
        {
            'user_id': notification_data['patient_id'],
            'message': get_text("appointment_notification_for_patient_message", patient['language'])
            .format(doctor['name'],
                    notification_data['date'],
                    notification_data['time']),
            'end_date': end_date,
            'start_date': date,
            'time_notifications': [{'time': one_hour_before}]
        },
        # Уведомление для доктора, ровно в день приема
        {
            'user_id': doctor['id'],
            'message': get_text("appointment_notification_for_doctor_message", doctor['language'])
            .format(patient['name'],
                    notification_data['date'],
                    notification_data['time']),
            'end_date': end_date,
            'start_date': date,
            'time_notifications': [{'time': notification_data['time']}]
        },
    ]
    return notifications
