from __future__ import annotations

from sqlalchemy import Text, CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class News(Base):
    __tablename__ = 'news'

    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    __table_args__ = (
        CheckConstraint(
            'length(content) <= 2000',
            name='comment_content_length'
        ),
    )
