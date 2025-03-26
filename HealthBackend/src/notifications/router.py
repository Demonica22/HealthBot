from fastapi import APIRouter, status

from src.database.session import SessionDep
from src.notifications.schemas import NotificationAddSchema, NotificationSchema
from src.notifications.service import NotificationsService

router = APIRouter(prefix="/notifications", tags=['Notifications'])


@router.post("/",
             response_model=NotificationSchema,
             status_code=status.HTTP_201_CREATED)
async def add_notification(data: NotificationAddSchema, session: SessionDep):
    return await NotificationsService.add_notification(data=data, session=session)


@router.get("/",
            response_model=list[NotificationSchema],
            status_code=status.HTTP_200_OK)
async def get_all_notifications(session: SessionDep):
    return await NotificationsService.get_all_notifications(session=session)


@router.delete("/{notification_id}")
async def delete_notification(notification_id: int, session: SessionDep):
    return await NotificationsService.delete_notification(notification_id=notification_id, session=session)


@router.get("/for_user/{user_id}",
            response_model=list[NotificationSchema],
            status_code=status.HTTP_200_OK)
async def get_notifications_for_user(user_id: int, session: SessionDep):
    return await NotificationsService.get_notifications_for_user(user_id=user_id, session=session)


@router.get("/schedule/{doctor_id}",
            response_model=list[NotificationSchema],
            status_code=status.HTTP_200_OK
            )
async def get_doctor_schedule(session: SessionDep, doctor_id: int):
    return await NotificationsService.get_doctor_schedule(session=session, doctor_id=doctor_id)
