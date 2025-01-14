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
    medicine_name: Mapped[str]
    end_date: Mapped[datetime.datetime]
    time_notifications: Mapped[list["NotificationTime"]] = relationship(back_populates="notification", uselist=True)


class NotificationTime(Base):
    __tablename__ = 'notification_times'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    notification_id: Mapped[int] = mapped_column(ForeignKey("notifications.id", ondelete="CASCADE"))
    notification: Mapped[Notification] = relationship(back_populates="time_notifications")
    time: Mapped[str]
