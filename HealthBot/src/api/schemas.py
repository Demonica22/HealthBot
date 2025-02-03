from pydantic import BaseModel, field_validator
from datetime import datetime
from src.utils.timezone import MSK


class DiseaseSchema(BaseModel):
    user_id: int
    id: int

    title: str
    description: str
    treatment_plan: str | None = None
    still_sick: bool
    date_from: datetime
    date_to: datetime | None = None


class NotificationSchema(BaseModel):
    id : int
    user_id: int
    message: str
    end_date: datetime
    start_date: datetime | None
    time_notifications: list[dict]

    @field_validator("end_date", "start_date", mode='before')
    def timestamp_to_date(cls, date) -> datetime | None:

        if not date:
            return None
        if not isinstance(date, str):
            raise TypeError(
                f"date expected a string value, received {date!r}"
            )
        return datetime.fromisoformat(date).replace(tzinfo=MSK)


class NotificationPostSchema(BaseModel):
    user_id: int
    message: str
    end_date: str
    start_date: str | None = None
    time_notifications: list[dict]

    @field_validator("end_date", "start_date", mode='before')
    def timestamp_to_date(cls, date) -> str | None:

        if not date:
            return None
        if not isinstance(date, datetime):
            raise TypeError(
                f"date expected a datetime value, received {date!r}"
            )
        return date.strftime("%d.%m.%Y %H:%M")
