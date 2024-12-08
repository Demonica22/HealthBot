from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    gender: str
    language: str
    weight: int
    height: int
