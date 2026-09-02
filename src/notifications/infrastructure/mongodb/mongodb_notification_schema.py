from motor.motor_asyncio import AsyncIOMotorCollection


async def create_notification_indexes(collection: AsyncIOMotorCollection) -> None:
    """Creates indexes for the notifications collection."""
    await collection.create_index("notification_id", unique=True)
