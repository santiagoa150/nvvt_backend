from typing import TypedDict


class UserDict(TypedDict):
    """Dictionary representation of a user."""

    user_id: str
    email: str
    password: str
    is_active: bool
