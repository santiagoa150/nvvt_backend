from orders.domain.order_dict import OrderDict
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject


class Order:
    """Represents an order in the system."""

    __slots__ = ("_order_id", "_client_id", "_client_quantity", "_product_id")

    def __init__(
        self,
        order_id: IdValueObject,
        client_id: IdValueObject,
        client_quantity: PositiveIntValueObject,
        product_id: IdValueObject,
    ):
        self._order_id = order_id
        self._client_id = client_id
        self._client_quantity = client_quantity
        self._product_id = product_id

    @property
    def order_id(self) -> IdValueObject:
        return self._order_id

    @property
    def client_quantity(self) -> PositiveIntValueObject:
        return self._client_quantity

    @client_quantity.setter
    def client_quantity(self, value: PositiveIntValueObject):
        self._client_quantity = value

    @property
    def product_id(self) -> IdValueObject:
        return self._product_id

    def to_dict(self) -> OrderDict:
        """Converts the order to a dictionary representation."""
        return OrderDict(
            order_id=self._order_id.str,
            client_id=self._client_id.str,
            client_quantity=self._client_quantity.int,
            product_id=self._product_id.str,
        )

    @classmethod
    def from_dict(cls, order_dict: OrderDict) -> "Order":
        """Creates an Order instance from a dictionary representation."""
        return cls(
            order_id=IdValueObject(order_dict["order_id"], "order_id"),
            client_id=IdValueObject(order_dict["client_id"], "client_id"),
            client_quantity=PositiveIntValueObject(
                order_dict["client_quantity"], "order_client_quantity"
            ),
            product_id=IdValueObject(order_dict["product_id"], "product_id"),
        )
