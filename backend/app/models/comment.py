from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User, Media

from sqlalchemy import ForeignKey, Text, text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Comment(Base):
    __tablename__ = 'comments'

    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    movie_id: Mapped[int] = mapped_column(ForeignKey('media.id'))
    to_comment_id: Mapped[int | None] = mapped_column(ForeignKey('comments.id'), nullable=True)
    is_published: Mapped[bool] = mapped_column(default=True, server_default=text('True'))

    user: Mapped[User] = relationship(
        'User', back_populates='comments'
    )

    movie: Mapped[Media] = relationship(
        'Media', back_populates='comments'
    )

    to_comment: Mapped[Comment | None] = relationship(
        'Comment', remote_side='Comment.id', back_populates='to_comments'
    )

    to_comments: Mapped[list[Comment]] = relationship(
        'Comment', back_populates='to_comment'
    )

    __table_args__ = (
        CheckConstraint(
            'length(content) <= 2000',
            name='comment_content_length'
        ),
    )
