from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User, Media

from sqlalchemy import ForeignKey, Text, text, CheckConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Comment(Base):
    __tablename__ = 'comments'

    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text('1'), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped[User] = relationship(
        'User', back_populates='comments'
    )

    movie_id: Mapped[int] = mapped_column(ForeignKey('media.id'), nullable=False)
    movie: Mapped[Media] = relationship(
        'Media', back_populates='comments'
    )

    to_comment_id: Mapped[int | None] = mapped_column(ForeignKey('comments.id'), nullable=True)
    to_comment: Mapped[Comment | None] = relationship(
        'Comment', remote_side='Comment.id', back_populates='replies'
    )

    replies: Mapped[list[Comment]] = relationship(
        'Comment', back_populates='to_comment'
    )

    __table_args__ = (
        CheckConstraint(
            'CHAR_LENGTH(content) <= 2000',
            name='comment_content_length'
        ),
    )
