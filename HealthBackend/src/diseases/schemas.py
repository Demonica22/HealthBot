import datetime

from typing import Optional
from pydantic import BaseModel, field_validator


class DiseaseSchemaAdd(BaseModel):
    user_id: int
    description: str
    date_from: datetime.datetime
    date_to: datetime.datetime | None = None

    still_sick: bool
    title: str
    treatment_plan: Optional[str]

    @field_validator("date_from", "date_to", mode='before')
    def timestamp_to_date(cls, date) -> datetime.datetime:

        if not date:
            return None
        if not isinstance(date, str):
            raise TypeError(
                f"date expected a string value, received {date!r}"
            )
        return datetime.datetime.strptime(date, "%d.%m.%Y")


class DiseaseSchema(DiseaseSchemaAdd):
    id: int

