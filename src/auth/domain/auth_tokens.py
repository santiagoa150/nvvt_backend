from typing import TypedDict


class AuthTokens(TypedDict):
    """Dictionary representation of authentication tokens."""

    access_token: str
    refresh_token: str
