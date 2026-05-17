from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import UserProfile, Comment, Genre

from sqlalchemy import CheckConstraint, Text, String, Enum as SAEnum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import favorite_media, media_genres

from db.base import Base

from utils.choices.content_type import ContentType


class Media(Base):
    __tablename__ = 'media'

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    type: Mapped[ContentType] = mapped_column(SAEnum(ContentType), nullable=False)
    seasons_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    genres: Mapped[list[Genre]] = relationship(secondary=media_genres)

    favorited_by: Mapped[list[UserProfile]] = relationship(
        secondary=favorite_media,
        back_populates='favorites'
    )

    comments: Mapped[list[Comment]] = relationship(
        'Comment', back_populates='movie', cascade='all, delete-orphan'
    )

    __table_args__ = (
        CheckConstraint(
            'length(description) <= 2000',
            name='comment_content_length'
        ),
        CheckConstraint(
            'seasons_count BETWEEN 1 AND 200',
            name='check_seasons_count_range'
        ),
    )
