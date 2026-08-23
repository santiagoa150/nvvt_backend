from typing import List

from products.domain.exceptions.product_exception import ProductException
from products.domain.product_dict import ProductDict
from products.domain.product_status import ProductStatus
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.int_value_object import IntValueObject
from shared.domain.value_objects.positive_float_value_object import (
    PositiveFloatValueObject,
)
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject
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
        "_installment_amounts",
        "_quantity",
        "_installments",
        "_page",
        "_status",
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
        installment_amounts: List[PositiveFloatValueObject],
        quantity: IntValueObject,
        installments: PositiveIntValueObject,
        page: PositiveIntValueObject,
        status: ProductStatus,
    ):
        if len(installment_amounts) != installments.int:
            raise ProductException.invalid_installment_amounts_size(
                installments.int, len(installment_amounts)
            )

        self._product_id = product_id
        self._campaign_id = campaign_id
        self._code = code
        self._name = name
        self._image_url = image_url
        self._catalog_price = catalog_price
        self._list_price = list_price
        self._installment_amounts = installment_amounts
        self._quantity = quantity
        self._installments = installments
        self._page = page
        self._status = status

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
    def image_url(self) -> StringValueObject:
        return self._image_url

    @property
    def catalog_price(self) -> PositiveFloatValueObject:
        return self._catalog_price

    @property
    def list_price(self) -> PositiveFloatValueObject:
        return self._list_price

    @property
    def installment_amounts(self) -> List[PositiveFloatValueObject]:
        return self._installment_amounts

    @property
    def quantity(self) -> IntValueObject:
        return self._quantity

    @property
    def installments(self) -> PositiveIntValueObject:
        return self._installments

    @property
    def page(self) -> PositiveIntValueObject:
        return self._page

    @property
    def status(self) -> ProductStatus:
        return self._status

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
            installment_amounts=[amount.float for amount in self._installment_amounts],
            quantity=self._quantity.int,
            installments=self._installments.int,
            page=self._page.int,
            status=self._status.value,
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
            installment_amounts=[
                PositiveFloatValueObject(float(amount), "product_installment_amount")
                for amount in product_dict["installment_amounts"]
            ],
            quantity=IntValueObject(product_dict["quantity"], "product_quantity", min_value=0),
            installments=PositiveIntValueObject(
                product_dict["installments"], "product_installments"
            ),
            page=PositiveIntValueObject(product_dict["page"], "product_page"),
            status=ProductStatus.create(product_dict["status"]),
        )
