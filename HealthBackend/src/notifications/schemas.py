import datetime

from typing import Optional
from pydantic import BaseModel,field_validator
from src.utils.constants import STRING_DATE_FORMAT

class NotificationTimeSchema(BaseModel):
    time: str


class NotificationAddSchema(BaseModel):
    user_id: int
    medicine_name: str
    end_date: datetime.datetime
    time_notifications: list[str] = None

    @field_validator("end_date", mode='before')
    def timestamp_to_date(cls, date) -> datetime.datetime:

        if not date:
            return None
        if not isinstance(date, str):
            raise TypeError(
                f"date expected a string value, received {date!r}"
            )
        return datetime.datetime.strptime(date, STRING_DATE_FORMAT)


class NotificationSchema(BaseModel):
    id: int
    user_id: int
    medicine_name: str
    end_date: datetime.datetime
    time_notifications: list[NotificationTimeSchema] = None
