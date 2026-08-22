from typing import TypedDict


class ProductProviderDict(TypedDict):
    """Dictionary representation of a product provider."""

    session_id: str
    route: str
    accelerator_secure_guid: str
    cebs_p: str
    cebs: str
