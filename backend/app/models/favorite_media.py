from sqlalchemy import Table, Column, ForeignKey

from db.base import Base

favorite_media = Table(
    'favorite_media',
    Base.metadata,
    Column('user_id', ForeignKey('user_profiles.id', ondelete='CASCADE'), primary_key=True),
    Column('media_id', ForeignKey('media.id', ondelete='CASCADE'), primary_key=True)
)
