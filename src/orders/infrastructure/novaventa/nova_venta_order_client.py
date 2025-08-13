import logging

import requests
from bs4 import BeautifulSoup

from orders.domain.exceptions.product_provider_exception import ProductProviderException
from orders.domain.product.product import Product
from orders.domain.product.product_dict import ProductDict
from orders.domain.product.product_provider import ProductProvider
from orders.domain.repository.order_client import OrderClient
from settings import settings
from shared.domain.value_objects.str_value_object import StringValueObject


class NovaVentaOrderClient(OrderClient):
    """Nova Venta Order Client for handling order operations."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    async def build_product(
        self, provider: ProductProvider, product_url: StringValueObject
    ) -> Product:
        headers = {
            "User-Agent": settings.nova_venta_user_agent,
            "Referer": settings.nova_venta_referer,
        }

        cookies = {
            "JSESSIONID": provider.session_id.str,
            "ROUTE": provider.route.str,
            "acceleratorSecureGUID": provider.accelerator_secure_guid.str,
            "cebsp": provider.cebs_p.str,
            "cebs": provider.cebs.str,
        }

        try:
            response = requests.get(product_url.str, headers=headers, cookies=cookies)
        except Exception:
            self._logger.error(f"Invalid product URL: {product_url.str}")
            raise ProductProviderException.invalid_product_url(product_url.str)

        if response and response.status_code != 200:
            self._logger.error(f"Failed to fetch product from Nova Venta: {response.status_code}")
            raise ProductProviderException.cannot_get_product_provider()

        soup = BeautifulSoup(response.text, "lxml")

        login_heading = soup.find("h3", class_="n-login--subheading")
        if login_heading:
            self._logger.error("Nova Venta login required, cannot fetch product.")
            raise ProductProviderException.expired_provider_credentials()

        try:
            raw_code = soup.find("span", class_="pdp--mark bold txt-regular no-margin")
            split_code = raw_code.text.split(" ⋅ ")
            code = split_code[0] if len(split_code) == 1 else split_code[1]

            raw_name = soup.find("h1", class_="pdp--name hidden-xs")
            name = raw_name.text.strip()

            raw_img_url = soup.find("img", class_="lazyOwl")
            image_url = raw_img_url["data-src"].strip()

            raw_catalog_price = soup.find("span", class_="regular__pdp--catalogprice--price")
            catalog_price = (
                raw_catalog_price.text.replace("$", "").replace(".", "").replace(",", ".").strip()
            )

            raw_list_price = soup.find("span", class_="regular__pdp--listprice--price")
            list_price = (
                raw_list_price.text.replace("$", "").replace(".", "").replace(",", ".").strip()
            )

            product = Product.from_dict(
                ProductDict(
                    image_url=image_url,
                    list_price=float(list_price),
                    catalog_price=float(catalog_price),
                    code=code,
                    name=name,
                )
            )
        except Exception as e:
            self._logger.error(f"Scraping error for product URL: {product_url.str} - {e}")
            raise ProductProviderException.cannot_build_product_data()

        return product
