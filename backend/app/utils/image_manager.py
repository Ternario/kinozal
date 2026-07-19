import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.utils.choices.content_type import ContentType
from config import settings


def save_image(file: UploadFile, media_type: ContentType) -> str:
    folder: str = media_type.name.lower()

    upload_dir: Path = settings.UPLOAD_DIR / folder
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext: str = file.filename.split('.')[-1]
    filename: str = f'{uuid.uuid4()}.{ext}'
    path: Path = upload_dir / filename

    with path.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f'{folder}/{filename}'


def delete_image(path: str) -> None:
    file_path: Path = Path('static') / path.lstrip('/')

    if file_path.exists():
        file_path.unlink()
