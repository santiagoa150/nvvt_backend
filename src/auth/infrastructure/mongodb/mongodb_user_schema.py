from motor.motor_asyncio import AsyncIOMotorCollection


async def create_user_indexes(collection: AsyncIOMotorCollection) -> None:
    """Create indexes for the user collection."""

    await collection.create_index('user_id', unique=True)
    await collection.create_index('email', unique=True)
