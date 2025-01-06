import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database.models import Base

class Disease(Base):
    __tablename__ = 'diseases'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="diseases")
    title: Mapped[str]
    description: Mapped[str]
    treatment_plan: Mapped[Optional[str]]
    date_from: Mapped[datetime.datetime]
    date_to: Mapped[Optional[datetime.datetime]]
    still_sick: Mapped[bool]
