from typing import TypedDict


class PhoneDict(TypedDict):
    """Dictionary representation of a phone number."""

    country_code: int
    number: int
