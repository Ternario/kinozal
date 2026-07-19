from sqlalchemy import Table, Column, ForeignKey, Integer

from db.base import Base

media_genres = Table(
    'media_genres',
    Base.metadata,
    Column(
        'media_id', Integer,
        ForeignKey('media.id', ondelete='CASCADE'),
        primary_key=True, nullable=False
    ),
    Column(
        'genre_id', Integer,
        ForeignKey('genres.id', ondelete='CASCADE'),
        primary_key=True, nullable=False
    ),
)
