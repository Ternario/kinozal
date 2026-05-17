from enum import Enum


class ContentType(str, Enum):
    """
    Types of media content.
    """

    MOVIE = 'movie'
    SERIES = 'series'
    ANIMATION = 'animation'
