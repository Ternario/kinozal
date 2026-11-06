from __future__ import annotations

from datetime import date

from pydantic import (
    BaseModel, ConfigDict, Field, HttpUrl, computed_field, model_validator
)

from app.schemas.genre import GenreRead
from app.utils.choices.content_type import ContentType
from config import settings
from utils.media import build_media_url


class MediaBase(BaseModel):
    title: str = Field(min_length=7, max_length=255)
    description: str = Field(min_length=50, max_length=5000)
    type: ContentType
    seasons_count: int | None = Field(default=None, ge=1, le=200)
    release_date: date
    trailer: str = Field(max_length=500)


class MediaCreate(MediaBase):
    genre_ids: list[int] = Field(..., min_length=1)

    @model_validator(mode='after')
    def validate_seasons(self):
        if self.type == ContentType.SERIES and self.seasons_count is None:
            raise ValueError('Season count is required for series.')

        if self.type == ContentType.MOVIE and self.seasons_count is not None:
            raise ValueError('Only series can have seasons count.')

        return self


class MediaUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=7, max_length=255)
    description: str | None = Field(default=None, min_length=50, max_length=5000)
    type: ContentType | None = None
    seasons_count: int | None = Field(default=None, ge=1, le=200)
    genre_ids: list[int] | None = Field(default=None)
    release_date: date | None = None
    trailer: str | None = Field(default=None, max_length=500)

    # @model_validator(mode='after')
    # def validate_seasons(self):
    #     if self.type == ContentType.SERIES and self.seasons_count is None:
    #         raise ValueError('Season count is required for series.')
    #
    #     if self.type == ContentType.MOVIE and self.seasons_count is not None:
    #         raise ValueError('Only series can have seasons count.')
    #
    #     return self


class MediaRead(MediaBase):
    id: int
    genres: list[GenreRead] = []

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def image_url(self) -> str | None:
        if not getattr(self, 'image_path', None):
            return None

        return build_media_url(self.image_path)
