import json
from collections.abc import Sequence

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from app.models import Media
from app.schemas.media import MediaRead, MediaCreate, MediaUpdate
from app.services.media_service import MediaService
from db.engine import get_session

router = APIRouter(prefix='/media', tags=['Media'])


def get_media_create_data(data: str = Form(...)) -> MediaCreate:
    try:
        return MediaCreate.model_validate(json.loads(data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Invalid JSON format: {str(e)}')


def get_media_update_data(data: str = Form(...)) -> MediaUpdate:
    try:
        return MediaUpdate.model_validate(json.loads(data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Invalid JSON format: {str(e)}')


@router.get('/', response_model=list[MediaRead], status_code=status.HTTP_200_OK)
async def get_media_list(
        skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)
) -> Sequence[Media]:
    return await MediaService.get_list(session=session, skip=skip, limit=limit)


@router.get('/{media_id}', response_model=MediaRead, status_code=status.HTTP_200_OK)
async def get_media_by_id(media_id: int, session: AsyncSession = Depends(get_session)) -> Media:
    media_by_id: Media | None = await MediaService.get_by_id(session=session, media_id=media_id)

    if not media_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Media with id {media_id} not found'
        )

    return media_by_id


@router.post('/', response_model=MediaRead, status_code=status.HTTP_201_CREATED)
async def create_media(
        data: Annotated[MediaCreate, Depends(get_media_create_data)],
        image: UploadFile | None = File(None),
        session: AsyncSession = Depends(get_session)
) -> Media:
    return await MediaService.create(session=session, data=data, image=image)


@router.put('/{media_id}', response_model=MediaRead, status_code=status.HTTP_200_OK)
async def update_media(
        media_id: int,
        data: Annotated[MediaUpdate, Depends(get_media_update_data)],
        image: UploadFile | None = File(None),
        session: AsyncSession = Depends(get_session)
) -> Media:
    try:
        return await MediaService.update(session=session, media_id=media_id, data=data, image=image)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete('/{media_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(media_id: int, session: AsyncSession = Depends(get_session)) -> None:
    try:
        await MediaService.delete(session=session, media_id=media_id)
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
