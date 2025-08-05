from orders.domain.order_dict import OrderDict
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_float_value_object import PositiveFloatValueObject
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject
from shared.domain.value_objects.string_value_object import StringValueObject


class Order:
    """Represents an order in the system."""
    __slots__ = ("_order_id", "_campaign_id", "_client_id", "_code", "_name", "_quantity", "_catalog_price",
                 "_list_price")

    def __init__(
            self,
            order_id: IdValueObject,
            campaign_id: IdValueObject,
            client_id: IdValueObject,
            code: StringValueObject,
            name: StringValueObject,
            quantity: PositiveIntValueObject,
            catalog_price: PositiveFloatValueObject,
            list_price: PositiveFloatValueObject,
    ):
        self._order_id = order_id
        self._campaign_id = campaign_id
        self._client_id = client_id
        self._code = code
        self._name = name
        self._quantity = quantity
        self._catalog_price = catalog_price
        self._list_price = list_price

    def to_dict(self) -> OrderDict:
        """Converts the order to a dictionary representation."""
        return OrderDict(
            order_id=self._order_id.str,
            campaign_id=self._campaign_id.str,
            client_id=self._client_id.str,
            code=self._code.str,
            name=self._name.str,
            quantity=self._quantity.int,
            catalog_price=self._catalog_price.float,
            list_price=self._list_price.float
        )

    @classmethod
    def from_dict(cls, order_dict: OrderDict) -> "Order":
        """Creates an Order instance from a dictionary representation."""
        return cls(
            order_id=IdValueObject(order_dict["order_id"], "order_id"),
            campaign_id=IdValueObject(order_dict["campaign_id"], "campaign_id"),
            client_id=IdValueObject(order_dict["client_id"], "client_id"),
            code=StringValueObject(order_dict["code"], "order_code"),
            name=StringValueObject(order_dict["name"], "order_name"),
            quantity=PositiveIntValueObject(order_dict["quantity"], "order_quantity"),
            catalog_price=PositiveFloatValueObject(order_dict["catalog_price"], "order_catalog_price"),
            list_price=PositiveFloatValueObject(order_dict["list_price"], "order_list_price")
        )
