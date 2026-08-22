import logging
from typing import List

from products.application.query.get.products_by_ids.get_products_by_ids_query import (
    GetProductsByIdsQuery,
)
from products.domain.product import Product
from products.domain.repository.product_read_repository import ProductReadRepository
from shared.domain.cqrs.query.iquery_handler import IQueryHandler


class GetProductsByIdsQueryHandler(IQueryHandler[GetProductsByIdsQuery]):
    """Handler for the GetProductsByIdsQuery."""

    def __init__(self, repository: ProductReadRepository):
        """
        :param repository: The product repository to use for fetching products.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, query: GetProductsByIdsQuery) -> List[Product]:
        """
        Handle the GetProductsByIdsQuery to retrieve products matching the given IDs.

        :param query: The query containing the product IDs.
        :return: The list of matching products.
        """
        self._logger.info(f"INIT :: Fetching {len(query.product_ids)} products")
        return await self._repository.get_products_by_ids(query.product_ids)
