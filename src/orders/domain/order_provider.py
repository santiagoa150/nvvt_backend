from orders.domain.order_provider_dict import OrderProviderDict
from shared.domain.value_objects.string_value_object import StringValueObject


class OrderProvider:
    """Represents an order provider in the system."""

    __slots__ = ("_session_id", "_route", "_accelerator_secure_guid", "_cebs_p", "_cebs")

    def __init__(
            self,
            session_id: StringValueObject,
            route: StringValueObject,
            accelerator_secure_guid: StringValueObject,
            cebs_p: StringValueObject,
            cebs: StringValueObject
    ):
        self._session_id = session_id
        self._route = route
        self._accelerator_secure_guid = accelerator_secure_guid
        self._cebs_p = cebs_p
        self._cebs = cebs

    @property
    def session_id(self) -> StringValueObject:
        return self._session_id

    @property
    def route(self) -> StringValueObject:
        return self._route

    @property
    def accelerator_secure_guid(self) -> StringValueObject:
        return self._accelerator_secure_guid

    @property
    def cebs_p(self) -> StringValueObject:
        return self._cebs_p

    @property
    def cebs(self) -> StringValueObject:
        return self._cebs

    def to_dict(self) -> OrderProviderDict:
        """Converts the order provider to a dictionary representation."""
        return OrderProviderDict(
            session_id=self._session_id.str,
            route=self._route.str,
            accelerator_secure_guid=self._accelerator_secure_guid.str,
            cebs_p=self._cebs_p.str,
            cebs=self._cebs.str
        )

    @classmethod
    def from_dict(cls, order_provider_dict: OrderProviderDict) -> "OrderProvider":
        """Creates an OrderProvider instance from a dictionary representation."""
        return cls(
            session_id=StringValueObject(order_provider_dict["session_id"], "session_id"),
            route=StringValueObject(order_provider_dict["route"], "route"),
            accelerator_secure_guid=StringValueObject(
                order_provider_dict["accelerator_secure_guid"], "accelerator_secure_guid"
            ),
            cebs_p=StringValueObject(order_provider_dict["cebs_p"], "cebs_p"),
            cebs=StringValueObject(order_provider_dict["cebs"], "cebs")
        )
