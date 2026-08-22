from motor.motor_asyncio import AsyncIOMotorCollection


async def create_order_indexes(collection: AsyncIOMotorCollection) -> None:
    """Creates indexes for the orders collection."""
    await collection.create_index("order_id", unique=True)
    # Enforces at most one order per client per product, and supports
    # get_order_by_client_and_product.
    await collection.create_index(["client_id", "product_id"], unique=True)
    # Supports get_orders_by_product_ids, used to resolve a campaign's orders.
    await collection.create_index("product_id")
