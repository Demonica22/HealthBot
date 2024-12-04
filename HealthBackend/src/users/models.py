from sqlalchemy.orm import Mapped, mapped_column
from src.database.models import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    gender: Mapped[str]
    language: Mapped[str]
    weight: Mapped[int]
    height: Mapped[int]
