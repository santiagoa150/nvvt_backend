from typing import List

from campaigns.domain.campaign_summary_dict import CampaignSummaryDict
from products.domain.product import Product
from shared.domain.value_objects.float_value_object import FloatValueObject


class CampaignSummary:
    """Represents a campaign's aggregated pricing summary, calculated from its products."""

    __slots__ = ("_total_catalog_price", "_total_list_price", "_profit")

    def __init__(
        self,
        total_catalog_price: FloatValueObject,
        total_list_price: FloatValueObject,
        profit: FloatValueObject,
    ):
        self._total_catalog_price = total_catalog_price
        self._total_list_price = total_list_price
        self._profit = profit

    @property
    def total_catalog_price(self) -> FloatValueObject:
        return self._total_catalog_price

    @property
    def total_list_price(self) -> FloatValueObject:
        return self._total_list_price

    @property
    def profit(self) -> FloatValueObject:
        return self._profit

    def to_dict(self) -> CampaignSummaryDict:
        """Converts the campaign summary to a dictionary representation."""
        return CampaignSummaryDict(
            total_catalog_price=self._total_catalog_price.float,
            total_list_price=self._total_list_price.float,
            profit=self._profit.float,
        )

    @classmethod
    def calculate(cls, products: List[Product]) -> "CampaignSummary":
        """Calculates a campaign's pricing summary from its products in a single pass."""
        total_catalog_price = 0.0
        total_list_price = 0.0

        for product in products:
            total_catalog_price += product.catalog_price.float * product.quantity.int
            total_list_price += product.list_price.float * product.quantity.int

        return cls(
            total_catalog_price=FloatValueObject(total_catalog_price, "total_catalog_price"),
            total_list_price=FloatValueObject(total_list_price, "total_list_price"),
            profit=FloatValueObject(total_catalog_price - total_list_price, "profit"),
        )
