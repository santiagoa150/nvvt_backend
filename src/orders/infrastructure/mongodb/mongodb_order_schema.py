from motor.motor_asyncio import AsyncIOMotorCollection


async def create_order_indexes(collection: AsyncIOMotorCollection) -> None:
    """Creates indexes for the orders collection."""
    await collection.create_index("order_id", unique=True)
