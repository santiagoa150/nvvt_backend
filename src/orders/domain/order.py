from orders.domain.order_dict import OrderDict
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_float_value_object import PositiveFloatValueObject
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject
from shared.domain.value_objects.string_value_object import StringValueObject


class Order:
    """Represents an order in the system."""
    __slots__ = ("_order_id", "_campaign_id", "_client_id", "_product_code", "_product_name", "_image_url", "_quantity",
                 "_catalog_price", "_list_price")

    def __init__(
            self,
            order_id: IdValueObject,
            campaign_id: IdValueObject,
            client_id: IdValueObject,
            product_code: StringValueObject,
            product_name: StringValueObject,
            image_url: StringValueObject,
            quantity: PositiveIntValueObject,
            catalog_price: PositiveFloatValueObject,
            list_price: PositiveFloatValueObject,
    ):
        self._order_id = order_id
        self._campaign_id = campaign_id
        self._client_id = client_id
        self._product_code = product_code
        self._product_name = product_name
        self._image_url = image_url
        self._quantity = quantity
        self._catalog_price = catalog_price
        self._list_price = list_price

    def to_dict(self) -> OrderDict:
        """Converts the order to a dictionary representation."""
        return OrderDict(
            order_id=self._order_id.str,
            campaign_id=self._campaign_id.str,
            client_id=self._client_id.str,
            product_code=self._product_code.str,
            product_name=self._product_name.str,
            image_url=self._image_url.str,
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
            product_code=StringValueObject(order_dict["product_code"], "product_code"),
            product_name=StringValueObject(order_dict["product_name"], "product_name"),
            image_url=StringValueObject(order_dict["image_url"], "order_image_url"),
            quantity=PositiveIntValueObject(order_dict["quantity"], "order_quantity"),
            catalog_price=PositiveFloatValueObject(float(order_dict["catalog_price"]), "order_catalog_price"),
            list_price=PositiveFloatValueObject(float(order_dict["list_price"]), "order_list_price")
        )
