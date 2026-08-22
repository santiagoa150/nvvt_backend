from typing import TypedDict


class CountryDict(TypedDict):
    """Dictionary representation of a country."""

    country_code: str
    country_name: str
    phone_code: int
