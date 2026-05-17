from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import UserProfile, Comment

from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str | None] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[str | None]
    is_staff: Mapped[bool] = mapped_column(default=False, server_default=text('false'))
    is_superuser: Mapped[bool] = mapped_column(default=False, server_default=text('false'))
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'))
    is_moderator: Mapped[bool] = mapped_column(default=False, server_default=text('false'))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text('true'))
    is_deleted: Mapped[bool] = mapped_column(default=False, server_default=text('false'))
    deleted_at: Mapped[datetime | None]

    profile: Mapped[UserProfile] = relationship(
        'UserProfile', back_populates='user', uselist=False, lazy='join'
    )

    comments: Mapped[Comment] = relationship(
        'Comment', back_populates='user', cascade='all, delete-orphan'
    )
