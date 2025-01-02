from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    gender: str
    language: str
    weight: int
    height: int


class UserPatchSchema(BaseModel):
    name: str | None = None
    gender: str | None = None
    language: str | None = None
    weight: int | None = None
    height: int | None = None
