from typing import List, TypedDict


class ScrapedProductDict(TypedDict):
    """Dictionary representation of raw product data scraped from an external provider."""

    code: str
    name: str
    image_url: str
    catalog_price: float
    list_price: float
    installment_amounts: List[float]
    installments: int
    page: int
