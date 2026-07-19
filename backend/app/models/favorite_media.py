from sqlalchemy import Table, Column, ForeignKey, Integer

from db.base import Base

favorite_media = Table(
    'favorite_media',
    Base.metadata,
    Column(
        'user_id', Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True, nullable=False
    ),
    Column(
        'media_id', Integer,
        ForeignKey('media.id', ondelete='CASCADE'),
        primary_key=True, nullable=False
    )
)
