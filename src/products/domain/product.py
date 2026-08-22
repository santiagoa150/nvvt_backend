from products.domain.product_dict import ProductDict
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_float_value_object import (
    PositiveFloatValueObject,
)
from shared.domain.value_objects.str_value_object import StringValueObject


class Product:
    """Represents a product belonging to a campaign."""

    __slots__ = (
        "_product_id",
        "_campaign_id",
        "_code",
        "_name",
        "_image_url",
        "_catalog_price",
        "_list_price",
    )

    def __init__(
        self,
        product_id: IdValueObject,
        campaign_id: IdValueObject,
        code: StringValueObject,
        name: StringValueObject,
        image_url: StringValueObject,
        catalog_price: PositiveFloatValueObject,
        list_price: PositiveFloatValueObject,
    ):
        self._product_id = product_id
        self._campaign_id = campaign_id
        self._code = code
        self._name = name
        self._image_url = image_url
        self._catalog_price = catalog_price
        self._list_price = list_price

    @property
    def product_id(self) -> IdValueObject:
        return self._product_id

    @property
    def campaign_id(self) -> IdValueObject:
        return self._campaign_id

    @property
    def code(self) -> StringValueObject:
        return self._code

    @property
    def name(self) -> StringValueObject:
        return self._name

    @property
    def catalog_price(self) -> PositiveFloatValueObject:
        return self._catalog_price

    @property
    def list_price(self) -> PositiveFloatValueObject:
        return self._list_price

    def to_dict(self) -> ProductDict:
        """Converts the product to a dictionary representation."""
        return ProductDict(
            product_id=self._product_id.str,
            campaign_id=self._campaign_id.str,
            code=self._code.str,
            name=self._name.str,
            image_url=self._image_url.str,
            catalog_price=self._catalog_price.float,
            list_price=self._list_price.float,
        )

    @classmethod
    def from_dict(cls, product_dict: ProductDict) -> "Product":
        """Creates a Product instance from a dictionary representation."""
        return cls(
            product_id=IdValueObject(product_dict["product_id"], "product_id"),
            campaign_id=IdValueObject(product_dict["campaign_id"], "campaign_id"),
            code=StringValueObject(product_dict["code"], "product_code"),
            name=StringValueObject(product_dict["name"], "product_name"),
            image_url=StringValueObject(product_dict["image_url"], "product_image_url"),
            catalog_price=PositiveFloatValueObject(
                float(product_dict["catalog_price"]), "product_catalog_price"
            ),
            list_price=PositiveFloatValueObject(
                float(product_dict["list_price"]), "product_list_price"
            ),
        )
