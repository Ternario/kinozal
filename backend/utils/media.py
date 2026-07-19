from config import settings


def build_media_url(path: str) -> str:
    return f'{settings.BASE_URL}/static/media/{path}'
