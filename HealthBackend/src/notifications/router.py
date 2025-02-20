from fastapi import APIRouter, status
from sqlalchemy import select, delete, cast, Date
from sqlalchemy.orm import selectinload

from src.database.session import SessionDep
from src.notifications.models import Notification, NotificationTime
from src.notifications.schemas import NotificationAddSchema, NotificationSchema

router = APIRouter(prefix="/notifications", tags=['Notifications'])


@router.post("/",
             response_model=NotificationSchema,
             status_code=status.HTTP_201_CREATED)
async def add_notification(data: NotificationAddSchema, session: SessionDep):
    data = data.model_dump()
    data['time_notifications'] = [NotificationTime(**elem) for elem in data['time_notifications']]
    notification = Notification(
        **data
    )
    session.add(notification)
    await session.commit()

    return notification


@router.get("/",
            response_model=list[NotificationSchema],
            status_code=status.HTTP_200_OK)
async def get_all_notifications(session: SessionDep):
    query = select(Notification).options(
        selectinload(Notification.time_notifications))
    result = await session.execute(query)

    return result.scalars().all()


@router.delete("/{notification_id}")
async def delete_notification(notification_id: int, session: SessionDep):
    try:
        query = delete(Notification).where(Notification.id == notification_id)
        await session.execute(query)
    except Exception as ex:
        await session.rollback()
        return {"success": False, "message": ex}
    else:
        await session.commit()
        return {"success": True}


@router.get("/for_user/{user_id}",
            response_model=list[NotificationSchema],
            status_code=status.HTTP_200_OK)
async def get_notifications_for_user(user_id: int, session: SessionDep):
    query = (select(Notification)
             .where(Notification.user_id == user_id)
             .options(selectinload(Notification.time_notifications)))
    result = await session.execute(query)

    return result.scalars().all()


@router.get("/schedule/{doctor_id}",
            response_model=list[NotificationSchema],
            status_code=status.HTTP_200_OK
            )
async def get_doctor_schedule(session: SessionDep, doctor_id: int):
    query = ((select(Notification)
              .where(Notification.user_id == doctor_id)
              .where(cast(Notification.end_date, Date) == cast(Notification.start_date, Date))
              .where(Notification.is_patient == False)
              .options(selectinload(Notification.time_notifications)))
             .order_by(Notification.end_date))
    result = await session.execute(query)

    return result.scalars().all()
