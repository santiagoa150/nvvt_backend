from typing import Optional

from clients.domain.client_dict import ClientDict
from shared.domain.phone import Phone
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.string_value_object import StringValueObject


class Client:
    """Represents a client in the system with its associated properties."""

    def __init__(
            self,
            client_id: IdValueObject,
            given_names: StringValueObject,
            family_names: Optional[StringValueObject],
            delivery_place: StringValueObject,
            phone: Optional[Phone],
    ):
        self._client_id = client_id
        self._given_names = given_names
        self._family_names = family_names
        self._delivery_place = delivery_place
        self._phone = phone

    def to_dict(self) -> ClientDict:
        """Converts the client to a dictionary representation."""
        return ClientDict(
            client_id=self._client_id.str,
            given_names=self._given_names.str,
            family_names=self._family_names.str if self._family_names else None,
            delivery_place=self._delivery_place.str,
            phone=self._phone.to_dict() if self._phone else None
        )

    @classmethod
    def from_dict(cls, client_dict: ClientDict) -> "Client":
        """Creates a Client instance from a dictionary representation."""
        return cls(
            client_id=IdValueObject(client_dict["client_id"], "client_id"),
            given_names=StringValueObject(client_dict["given_names"], "given_names"),
            family_names=StringValueObject(client_dict["family_names"], "family_names") if client_dict.get("family_names") else None,
            delivery_place=StringValueObject(client_dict["delivery_place"], "delivery_place"),
            phone=Phone.from_dict(client_dict["phone"]) if client_dict.get("phone") else None
        )
