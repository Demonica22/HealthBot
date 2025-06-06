from pydantic import BaseModel, ConfigDict

class UserSchema(BaseModel):
    id: int
    name: str
    gender: str
    language: str
    weight: int
    height: int


    model_config = ConfigDict(from_attributes=True)


class UserPatchSchema(BaseModel):
    name: str | None = None
    gender: str | None = None
    language: str | None = None
    weight: int | None = None
    height: int | None = None
    doctor_id: int | None = None
