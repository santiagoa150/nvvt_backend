import logging

import requests

from campaigns.application.query import GetCampaignByIdQuery
from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_status import CampaignStatus
from products.application.command.create_product.create_product_command import (
    CreateProductCommand,
)
from products.domain.exceptions.product_already_exists_exception import (
    ProductAlreadyExistsException,
)
from products.domain.exceptions.product_exception import ProductException
from products.domain.exceptions.product_provider_exception import ProductProviderException
from products.domain.product import Product
from products.domain.product_provider import ProductProvider
from products.domain.product_status import ProductStatus
from products.domain.repository.product_client import ProductClient
from products.domain.repository.product_read_repository import ProductReadRepository
from products.domain.repository.product_write_repository import ProductWriteRepository
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.repository.campaign_file_storage import CampaignFileStorage
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.str_value_object import StringValueObject


class CreateProductCommandHandler(ICommandHandler[CreateProductCommand]):
    """Handler for the CreateProductCommand."""

    def __init__(
        self,
        query_bus: QueryBus,
        read_repository: ProductReadRepository,
        write_repository: ProductWriteRepository,
        product_client: ProductClient,
        campaign_file_storage: CampaignFileStorage,
    ):
        """
        :param query_bus: The query bus to use for querying the campaign.
        :param read_repository: The product repository to use for the existence check.
        :param write_repository: The product repository to use for creating the product.
        :param product_client: The client to use for fetching product data from the provider.
        :param campaign_file_storage: The storage used to persist the product's image.
        """
        self._query_bus = query_bus
        self._read_repository = read_repository
        self._write_repository = write_repository
        self._product_client = product_client
        self._campaign_file_storage = campaign_file_storage
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: CreateProductCommand) -> None:
        """
        Handle the CreateProductCommand to create a new product for a campaign.

        :param command: The command containing the product details.
        :raises NotFoundException: If the campaign doesn't exist.
        :raises ProductException: If the campaign isn't active.
        :raises ProductAlreadyExistsException: If the product already exists for the campaign.
        """
        self._logger.info(
            f"INIT :: Creating Product with code {command.code.str} "
            f"for Campaign {command.campaign_id.str}"
        )

        campaign: Campaign = await self._query_bus.query(GetCampaignByIdQuery(command.campaign_id))

        if campaign.status != CampaignStatus.ACTIVE:
            raise ProductException.campaign_not_active(command.campaign_id.str)

        if await self._read_repository.exists_by_campaign_and_code(
            command.campaign_id, command.code
        ):
            raise ProductAlreadyExistsException.already_exists_for_campaign(
                command.campaign_id.str, command.code.str
            )

        provider = ProductProvider(provider_token=command.provider_token, cart_id=None)
        scraped_product = await self._product_client.build_product(
            provider, command.code, campaign.number
        )

        image_url = self._store_image(command.campaign_id, command.code, scraped_product.image_url)

        product = Product(
            product_id=IdValueObject(IdValueObject.generate(), "product_id"),
            campaign_id=command.campaign_id,
            code=scraped_product.code,
            name=scraped_product.name,
            image_url=image_url,
            catalog_price=scraped_product.catalog_price,
            list_price=scraped_product.list_price,
            installment_amounts=scraped_product.installment_amounts,
            quantity=command.quantity,
            installments=scraped_product.installments,
            page=scraped_product.page,
            status=ProductStatus.ACTIVE,
        )

        await self._write_repository.create_product(product)

    def _store_image(
        self,
        campaign_id: IdValueObject,
        code: StringValueObject,
        source_url: StringValueObject,
    ) -> StringValueObject:
        """Downloads the product's image and stores it in the campaign's file folder."""
        try:
            response = requests.get(source_url.str)
            response.raise_for_status()
        except Exception:
            self._logger.error(f"Failed to download product image from: {source_url.str}")
            raise ProductProviderException.cannot_build_product_data()

        extension = source_url.str.rsplit(".", 1)[-1]
        file_name = f"{code.str}.{extension}"
        local_path = self._campaign_file_storage.save_file(
            campaign_id.str, file_name, response.content
        )
        return StringValueObject(local_path, "product_image_url")
