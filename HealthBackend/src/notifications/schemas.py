import datetime

from typing import Optional
from pydantic import BaseModel, field_validator
from src.utils.constants import DATE_TIME_FORMAT


class NotificationTimeSchema(BaseModel):
    time: str


class NotificationAddSchema(BaseModel):
    user_id: int
    message: str
    end_date: datetime.datetime
    start_date: datetime.datetime | None = None
    time_notifications: list[NotificationTimeSchema] = None
    is_patient: bool = True
    @field_validator("end_date", "start_date", mode='before')
    def timestamp_to_date(cls, date) -> datetime.datetime | None:

        if not date:
            return None
        if not isinstance(date, str):
            raise TypeError(
                f"date expected a string value, received {date!r}"
            )
        return datetime.datetime.strptime(date, DATE_TIME_FORMAT)


class NotificationSchema(BaseModel):
    id: int
    user_id: int
    message: str
    end_date: datetime.datetime
    start_date: datetime.datetime | None = None
    time_notifications: list[NotificationTimeSchema] = None
    is_patient: bool
