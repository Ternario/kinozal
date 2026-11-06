from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Comment, Genre, User

from datetime import date
from sqlalchemy import CheckConstraint, Text, String, Enum, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.favorite_media import favorite_media
from app.models.media_genres import media_genres

from db.base import Base

from app.utils.choices.content_type import ContentType


class Media(Base):
    __tablename__ = 'media'

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[ContentType] = mapped_column(Enum(ContentType), nullable=False)
    seasons_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    genres: Mapped[list[Genre]] = relationship('Genre', secondary=media_genres)
    release_date: Mapped[date] = mapped_column(Date, nullable=False)
    trailer: Mapped[str] = mapped_column(String(500), nullable=False)
    favorited_by: Mapped[list[User]] = relationship(
        'User', secondary=favorite_media, back_populates='favorites'
    )
    comments: Mapped[list[Comment]] = relationship(
        'Comment', back_populates='movie', cascade='all, delete-orphan'
    )

    __table_args__ = (
        CheckConstraint(
            'CHAR_LENGTH(title) BETWEEN 7 AND 255',
            name='check_media_title_length'
        ),
        CheckConstraint(
            'CHAR_LENGTH(description) BETWEEN 50 AND 5000',
            name='check_media_description_length'
        ),
        CheckConstraint(
            """
            (type = 'MOVIE' AND seasons_count IS NULL)
            OR
            (type = 'SERIES' AND seasons_count BETWEEN 1 AND 200)
            OR
            (type IN ('ANIMATION', 'DOCUMENTARY') AND seasons_count IS NULL)
            """,
            name='check_media_type_seasons'
        )
    )
