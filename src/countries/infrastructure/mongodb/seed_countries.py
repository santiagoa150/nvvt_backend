import asyncio
import json
import logging
from pathlib import Path

from countries.country_dependencies import get_countries_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SEED_FILE = Path(__file__).parent / "seed" / "countries_seed.json"


async def seed_countries() -> None:
    """Upserts the reference country / phone-code catalog into MongoDB, by country_code."""
    collection = await get_countries_collection()
    countries = json.loads(SEED_FILE.read_text(encoding="utf-8"))

    for country in countries:
        await collection.update_one(
            {"country_code": country["country_code"]},
            {"$set": country},
            upsert=True,
        )

    logger.info(f"Seeded {len(countries)} countries")


if __name__ == "__main__":
    asyncio.run(seed_countries())
