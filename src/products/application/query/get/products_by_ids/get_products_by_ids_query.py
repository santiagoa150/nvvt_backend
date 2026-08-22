from typing import List

from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.value_objects.id_value_object import IdValueObject


class GetProductsByIdsQuery(IQuery):
    """Query to get products matching the given IDs."""

    def __init__(self, product_ids: List[IdValueObject]):
        """
        :param product_ids: The IDs of the products to retrieve.
        """
        self.product_ids = product_ids
