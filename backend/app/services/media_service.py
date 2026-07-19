from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Media, Genre
from app.schemas.media import MediaUpdate, MediaCreate
from app.utils.choices.content_type import ContentType
from app.utils.image_manager import save_image, delete_image


class MediaService:
    # def _validate_type_and_seasons(self, type_, seasons):
    #     if type_ == "SERIES" and seasons is None:
    #         raise ValueError("Series must have seasons_count")
    #
    #     if type_ != "SERIES" and seasons is not None:
    #         raise ValueError("Only series can have seasons_count")
    #
    # def _validate(self, media: MediaCreate):
    #     is_series = media.type == ContentType.SERIES
    #
    #     if is_series and media.seasons_count is None:
    #         raise HTTPException(
    #             status_code=400,
    #             detail='Season count is required for series.'
    #         )
    #
    #     if not is_series and media.seasons_count is not None:
    #         raise HTTPException(
    #             status_code=400,
    #             detail='Only series can have seasons count.'
    #         )

    async def _get_genres(self, session: AsyncSession, genres_ids: list[int]) -> Sequence[Genre]:
        genres_set: set[int] = set(genres_ids)

        result: ScalarResult[Genre] = await session.scalars(
            select(Genre).where(Genre.id.in_(genres_set))
        )

        genres: Sequence[Genre] = result.all()

        if len(genres) != len(genres_set):
            raise HTTPException(
                status_code=400,
                detail='One or more genres do not exist.'
            )

        return genres

    async def create(self, session: AsyncSession, data: MediaCreate, image=None) -> Media:
        image_path: str | None = None

        try:
            if image:
                image_path: str = save_image(image, data.type)

            genres: Sequence[Genre] = await self._get_genres(session, data.genre_ids)

            media: Media = Media(**data.model_dump(exclude={'genre_ids'}), image_path=image_path)
            media.genres = genres

            session.add(media)
            await session.commit()
            await session.refresh(media)

            return media

        except Exception:
            await session.rollback()

            if image_path:
                delete_image(image_path)

            raise

    async def update(self, session: AsyncSession, media_id: int, data: MediaUpdate, image=None) -> Media:
        media: Media | None = await session.get(Media, media_id)

        if not media:
            raise ValueError('Media not found')

        old_img_path: str = media.image_path
        new_img_path: str | None = None

        try:
            updated_data: dict[str, Any] = data.model_dump(exclude_unset=True)

            new_type: ContentType = updated_data.get('type', media.type)

            if new_type == ContentType.MOVIE:
                new_seasons_count: int | None = None
            else:
                new_seasons_count: int | None = (
                    updated_data['seasons_count']
                    if 'seasons_count' in updated_data
                    else media.seasons_count
                )

            if image:
                new_img_path = save_image(image, new_type)
                media.image_path = new_img_path

            for field, value in updated_data.items():
                if field in ('type', 'seasons_count', 'genre_ids'):
                    continue

                setattr(media, field, value)

            media.type = new_type
            media.seasons_count = new_seasons_count

            if 'genre_ids' in updated_data:
                media.genres = await self._get_genres(session, updated_data['genre_ids'])

            await session.commit()
            await session.refresh(media)

            if new_img_path and old_img_path:
                delete_image(old_img_path)

            return media

        except Exception:
            await session.rollback()

            if new_img_path:
                delete_image(new_img_path)

            raise

    async def delete(self, session: AsyncSession, media_id: int) -> None:
        media: Media | None = await session.get(Media, media_id)

        if not media:
            raise ValueError('Media not found')

        img_path: str = media.image_path

        try:
            await session.delete(media)
            await session.commit()

        except Exception:
            await session.rollback()
            raise

        if img_path:
            delete_image(img_path)
