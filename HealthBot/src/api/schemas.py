from pydantic import BaseModel
from datetime import datetime


class DiseaseSchema(BaseModel):
    user_id: int

    title: str
    description: str
    treatment_plan: str | None = None
    still_sick: bool
    date_from: datetime
    date_to: datetime | None = None
