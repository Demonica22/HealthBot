import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database.models import Base


class Notification(Base):
    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="notifications")
    message: Mapped[str] = mapped_column(nullable=True)
    end_date: Mapped[datetime.datetime]
    start_date: Mapped[datetime.datetime] = mapped_column(nullable=True)
    time_notifications: Mapped[list["NotificationTime"]] = relationship(back_populates="notification", uselist=True)
    is_patient: Mapped[bool] = mapped_column(server_default='t')


class NotificationTime(Base):
    __tablename__ = 'notification_times'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    notification_id: Mapped[int] = mapped_column(ForeignKey("notifications.id", ondelete="CASCADE"))
    notification: Mapped[Notification] = relationship(back_populates="time_notifications")
    time: Mapped[str]
