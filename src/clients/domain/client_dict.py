from typing import TypedDict, Optional

from shared.domain.value_objects.phone_dict import PhoneDict


class ClientDict(TypedDict):
    """Dictionary representation of a client."""

    client_id: str
    given_names: str
    family_names: str
    delivery_place: str
    phone: Optional[PhoneDict]
