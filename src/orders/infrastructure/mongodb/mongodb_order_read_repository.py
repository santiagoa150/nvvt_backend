from typing import Optional, cast

from motor.motor_asyncio import AsyncIOMotorCollection

from orders.domain.order import Order
from orders.domain.order_dict import OrderDict
from orders.domain.repository.order_read_repository import OrderReadRepository
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.string_value_object import StringValueObject


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

    async def get_order_by_campaign_client_code(
            self,
            campaign_id: IdValueObject,
            client_id: IdValueObject,
            code: StringValueObject
    ) -> Optional[Order]:
        """Retrieve an order by its code associated with a specific campaign and client."""
        document = await self._collection.find_one({
            "campaign_id": campaign_id.str,
            "client_id": client_id.str,
            "product.code": code.str
        })

        if document is None:
            return None

        return Order.from_dict(cast(OrderDict, document))

    async def get_orders_by_campaign(
            self,
            campaign_id: IdValueObject,
            client_id: Optional[IdValueObject]
    ) -> dict[str, list[Order]]:
        """Retrieve all orders associated with a specific campaign ID."""
        filters = {"campaign_id": campaign_id.str}

        if client_id is not None:
            filters["client_id"] = client_id.str

        documents = await self._collection.find(filters).to_list(length=None)

        grouped: dict[str, list[Order]] = {}
        for doc in documents or []:
            order = Order.from_dict(cast(OrderDict, doc))
            grouped.setdefault(order.status.value, []).append(order)

        return grouped
