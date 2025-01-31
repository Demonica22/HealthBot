from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger

from src.database.models import Base


class Doctor(Base):
    __tablename__ = "doctors"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
