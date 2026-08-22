from orders.domain.order_dict import OrderDict
from orders.domain.order_status import OrderStatus
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject


class Order:
    """Represents an order in the system."""

    __slots__ = ("_order_id", "_client_id", "_quantity", "_status", "_product_id")

    def __init__(
        self,
        order_id: IdValueObject,
        client_id: IdValueObject,
        quantity: PositiveIntValueObject,
        status: OrderStatus,
        product_id: IdValueObject,
    ):
        self._order_id = order_id
        self._client_id = client_id
        self._quantity = quantity
        self._status = status
        self._product_id = product_id

    @property
    def order_id(self) -> IdValueObject:
        return self._order_id

    @property
    def quantity(self) -> PositiveIntValueObject:
        return self._quantity

    @quantity.setter
    def quantity(self, value: PositiveIntValueObject):
        self._quantity = value

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def product_id(self) -> IdValueObject:
        return self._product_id

    def to_dict(self) -> OrderDict:
        """Converts the order to a dictionary representation."""
        return OrderDict(
            order_id=self._order_id.str,
            client_id=self._client_id.str,
            quantity=self._quantity.int,
            status=self._status.value,
            product_id=self._product_id.str,
        )

    @classmethod
    def from_dict(cls, order_dict: OrderDict) -> "Order":
        """Creates an Order instance from a dictionary representation."""
        return cls(
            order_id=IdValueObject(order_dict["order_id"], "order_id"),
            client_id=IdValueObject(order_dict["client_id"], "client_id"),
            quantity=PositiveIntValueObject(order_dict["quantity"], "order_quantity"),
            status=OrderStatus.create(order_dict["status"]),
            product_id=IdValueObject(order_dict["product_id"], "product_id"),
        )
