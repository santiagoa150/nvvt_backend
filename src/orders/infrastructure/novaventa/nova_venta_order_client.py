import logging

import requests
from bs4 import BeautifulSoup

from settings import settings
from orders.domain.order_provider import OrderProvider
from orders.domain.product import Product
from orders.domain.repository.order_client import OrderClient
from shared.domain.value_objects.string_value_object import StringValueObject


class NovaVentaOrderClient(OrderClient):
    """Nova Venta Order Client for handling order operations."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    async def build_product(self, provider: OrderProvider, product_url: StringValueObject) -> Product:
        headers = {
            'User-Agent': settings.nova_venta_user_agent,
            'Referer': settings.nova_venta_referer,
        }

        cookies = {
            'JSESSIONID': provider.session_id.str,
            'ROUTE': provider.route.str,
            'acceleratorSecureGUID': provider.accelerator_secure_guid.str,
            'cebs_p': provider.cebs_p.str,
            'cebs': provider.cebs.str
        }

        response = requests.get(product_url.str, headers=headers, cookies=cookies)

        if response.status_code != 200:
            self._logger.error(f"Failed to fetch product from Nova Venta: {response.status_code}")
            raise Exception("Failed to fetch product details")
