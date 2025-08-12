from typing import TypedDict


class AuthData(TypedDict):
    """Dictionary representation of authentication data."""

    user_id: str
    email: str
