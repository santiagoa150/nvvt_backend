from typing import List, Optional, cast

from motor.motor_asyncio import AsyncIOMotorCollection

from orders.domain.order import Order
from orders.domain.order_dict import OrderDict
from orders.domain.repository.order_read_repository import OrderReadRepository
from shared.domain.value_objects.id_value_object import IdValueObject


class MongoDBOrderReadRepository(OrderReadRepository):
    """MongoDB implementation of the OrderReadRepository interface."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBOrderReadRepository with a MongoDB collection."""
        self._collection = collection

    async def get_order_by_id(self, order_id: IdValueObject) -> Optional[Order]:
        """Retrieve an order by its ID."""
        document = await self._collection.find_one({"order_id": order_id.str})

        if document is None:
            return None

        return Order.from_dict(cast(OrderDict, document))

    async def get_order_by_client_and_product(
        self, client_id: IdValueObject, product_id: IdValueObject
    ) -> Optional[Order]:
        """Retrieve the order a client placed for a specific product."""
        document = await self._collection.find_one(
            {"client_id": client_id.str, "product_id": product_id.str}
        )

        if document is None:
            return None

        return Order.from_dict(cast(OrderDict, document))

    async def get_orders_by_product_ids(
        self, product_ids: List[IdValueObject], client_id: Optional[IdValueObject]
    ) -> dict[str, list[Order]]:
        """Retrieve all orders placed for the given products."""
        if not product_ids:
            return {}

        filters = {"product_id": {"$in": [product_id.str for product_id in product_ids]}}

        if client_id is not None:
            filters["client_id"] = client_id.str

        documents = await self._collection.find(filters).to_list(length=None)

        grouped: dict[str, list[Order]] = {}
        for doc in documents or []:
            order = Order.from_dict(cast(OrderDict, doc))
            grouped.setdefault(order.status.value, []).append(order)

        return grouped
