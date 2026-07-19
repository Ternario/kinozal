from enum import Enum


class ContentType(str, Enum):
    """
    Types of media content.
    """

    MOVIE = 'Movie'
    SERIES = 'Series'
    ANIMATION = 'Animation'
