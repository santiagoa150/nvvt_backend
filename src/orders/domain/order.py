from orders.domain.order_dict import OrderDict
from orders.domain.product import Product
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject


class Order:
    """Represents an order in the system."""
    __slots__ = ("_order_id", "_campaign_id", "_client_id", "_quantity", "_product")

    def __init__(
            self,
            order_id: IdValueObject,
            campaign_id: IdValueObject,
            client_id: IdValueObject,
            quantity: PositiveIntValueObject,
            product: Product,
    ):
        self._order_id = order_id
        self._campaign_id = campaign_id
        self._client_id = client_id
        self._quantity = quantity
        self._product = product

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
    def product(self) -> Product:
        return self._product

    def to_dict(self) -> OrderDict:
        """Converts the order to a dictionary representation."""
        return OrderDict(
            order_id=self._order_id.str,
            campaign_id=self._campaign_id.str,
            client_id=self._client_id.str,
            quantity=self._quantity.int,
            product=self._product.to_dict()
        )

    @classmethod
    def from_dict(cls, order_dict: OrderDict) -> "Order":
        """Creates an Order instance from a dictionary representation."""
        return cls(
            order_id=IdValueObject(order_dict["order_id"], "order_id"),
            campaign_id=IdValueObject(order_dict["campaign_id"], "campaign_id"),
            client_id=IdValueObject(order_dict["client_id"], "client_id"),
            quantity=PositiveIntValueObject(order_dict["quantity"], "order_quantity"),
            product=Product.from_dict(order_dict["product"])
        )
