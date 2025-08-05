from typing import Optional, cast

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

    async def get_orders_by_campaign(self, campaign_id: IdValueObject) -> list[Order]:
        """Retrieve all orders associated with a specific campaign ID."""
        documents = await self._collection.find({"campaign_id": campaign_id.str}).to_list(length=None)

        return [Order.from_dict(cast(OrderDict, doc)) for doc in documents] if documents else []
