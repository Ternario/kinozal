from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import UserProfile, Comment, Media

from datetime import datetime, date

from sqlalchemy import text, String, Date, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from app.models.favorite_media import favorite_media


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str | None] = mapped_column(String(155), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(155), nullable=False)
    last_name: Mapped[str] = mapped_column(String(155), nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('0'), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('0'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('0'), nullable=False)
    is_moderator: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('0'), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text('1'), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('0'), nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    profile: Mapped[UserProfile] = relationship(
        'UserProfile', back_populates='user', uselist=False, lazy='joined'
    )

    comments: Mapped[Comment] = relationship(
        'Comment', back_populates='user', cascade='all, delete-orphan'
    )

    favorites: Mapped[list[Media]] = relationship(
        'Media', secondary=favorite_media, back_populates='favorited_by'
    )
