from motor.motor_asyncio import AsyncIOMotorCollection


async def create_client_indexes(collection: AsyncIOMotorCollection) -> None:
    """Creates indexes for the clients collection."""
    await collection.create_index('client_id', unique=True)
