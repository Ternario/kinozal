from sqlalchemy import Table, Column, ForeignKey

from db.base import Base

media_genres = Table(
    'media_genres',
    Base.metadata,
    Column('media_id', ForeignKey('media.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True),
)
