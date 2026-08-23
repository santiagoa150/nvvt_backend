import logging

import requests

from products.domain.exceptions.product_provider_exception import ProductProviderException
from products.domain.product_provider import ProductProvider
from products.domain.repository.product_client import ProductClient
from products.domain.scraped_product import ScrapedProduct
from products.domain.scraped_product_dict import ScrapedProductDict
from settings import settings
from shared.domain.value_objects.int_value_object import IntValueObject
from shared.domain.value_objects.str_value_object import StringValueObject

_UNAUTHORIZED_STATUS_CODES = (401, 403)


class NovaventaProductClient(ProductClient):
    """Novaventa Product Client for fetching product data."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    async def build_product(
        self, provider: ProductProvider, code: StringValueObject, campaign_number: IntValueObject
    ) -> ScrapedProduct:
        headers = {
            "Authorization": f"Bearer {provider.provider_token.str}",
        }

        search_url = settings.novaventa_product_search_url.format(code=code.str)

        try:
            response = requests.get(search_url, headers=headers)
        except Exception:
            self._logger.error(f"Failed to reach Novaventa for product code: {code.str}")
            raise ProductProviderException.cannot_get_product_provider()

        if response.status_code in _UNAUTHORIZED_STATUS_CODES:
            self._logger.error("Novaventa provider credentials have expired.")
            raise ProductProviderException.expired_provider_credentials()

        if response.status_code != 200:
            self._logger.error(f"Failed to fetch product from Novaventa: {response.status_code}")
            raise ProductProviderException.cannot_get_product_provider()

        products = response.json()
        if not products:
            self._logger.error(f"Product with code {code.str} was not found in Novaventa.")
            raise ProductProviderException.product_not_found_in_provider(code.str)

        try:
            raw_product = products[0]

            image_url = settings.novaventa_product_image_url.format(
                campaign_number=campaign_number.int, code=code.str
            )

            product = ScrapedProduct.from_dict(
                ScrapedProductDict(
                    code=str(raw_product["codigoCl"]),
                    name=raw_product["descripcion"],
                    image_url=image_url,
                    catalog_price=float(raw_product["precio"]),
                    list_price=float(raw_product["precioLista"]),
                    installment_amounts=[
                        float(amount) for amount in raw_product["cuotasNovaventa"]
                    ],
                    installments=int(raw_product["cuotas"]),
                    page=int(raw_product["page"]),
                )
            )
        except Exception as e:
            self._logger.error(f"Error building product data for code {code.str}: {e}")
            raise ProductProviderException.cannot_build_product_data()

        return product
