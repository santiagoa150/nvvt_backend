from motor.motor_asyncio import AsyncIOMotorCollection


async def create_campaign_indexes(collection: AsyncIOMotorCollection) -> None:
    """Creates indexes for the campaigns collection."""
    await collection.create_index("campaign_id", unique=True)
    await collection.create_index(["year", "number"], unique=True)
    await collection.create_index(
        "is_active", unique=True, partialFilterExpression={"is_active": True}
    )
    # Supports the paginated listing's sort: active campaign first, then year and
    # number descending. Ascending here is enough since MongoDB can satisfy a
    # fully-descending sort by scanning an ascending index backwards.
    await collection.create_index(["is_active", "year", "number"])
