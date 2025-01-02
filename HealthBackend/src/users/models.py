from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models import Base
# from src.diseases.models import Disease


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    diseases: Mapped[list["Disease"]] = relationship(back_populates="user")
    name: Mapped[str]
    gender: Mapped[str]
    language: Mapped[str]
    weight: Mapped[int]
    height: Mapped[int]
