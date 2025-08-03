from motor.motor_asyncio import AsyncIOMotorCollection


async def create_campaign_indexes(collection: AsyncIOMotorCollection) -> None:
    """Creates indexes for the campaigns collection."""
    await collection.create_index('campaign_id', unique=True)
    await collection.create_index(['year', 'number'], unique=True)
