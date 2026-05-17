from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User, Media

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.favorite_media import favorite_media
from db.base import Base
from utils.choices.theme import ProfileTheme


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        unique=True,
        nullable=False
    )  ### with or without this field
    user: Mapped[User] = relationship(
        'User', back_populates='profile', uselist=False
    )
    theme: Mapped[ProfileTheme] = mapped_column(default=ProfileTheme.LIGHT)
    receive_email_notifications: Mapped[bool] = mapped_column(default=True)
    favorites: Mapped[list[Media]] = relationship(
        secondary=favorite_media, back_populates='favorited_by'
    )
