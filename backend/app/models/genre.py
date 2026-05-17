from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Genre(Base):
    __tablename__ = 'genres'
    name: Mapped[str] = mapped_column(String(50), unique=True)


