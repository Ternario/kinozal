from sqlalchemy import String, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class SearchQuery(Base):
    __tablename__ = 'search_queries'

    query: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    searches_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    __table_args__ = (
        CheckConstraint(
            'searches_count >= 1',
            name='check_search_count_min_value'
        ),
    )
