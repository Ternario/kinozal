from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User

from sqlalchemy import ForeignKey, Boolean, text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from app.utils.choices.theme import ProfileTheme


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        unique=True,
        nullable=False
    )
    user: Mapped[User] = relationship(
        'User', back_populates='profile', uselist=False
    )
    theme: Mapped[ProfileTheme] = mapped_column(Enum(ProfileTheme), default=ProfileTheme.LIGHT)
    receive_email_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text('1'),
        nullable=False
    )
