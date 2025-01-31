from pydantic import BaseModel


class DoctorSchema(BaseModel):
    id: int
