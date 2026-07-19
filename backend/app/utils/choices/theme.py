from enum import Enum


class ProfileTheme(str, Enum):
    """
    Visual themes available for a user profile.

    - LIGHT: Light theme.
    - DARK: Dark theme.
    """
    LIGHT = 'light'
    DARK = 'dark'
