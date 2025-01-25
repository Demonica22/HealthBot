from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger

from src.database.models import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    diseases: Mapped[list["Disease"]] = relationship(back_populates="user")
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user")
    name: Mapped[str]
    gender: Mapped[str]
    language: Mapped[str]
    weight: Mapped[int]
    height: Mapped[int]
    doctor_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)
