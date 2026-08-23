import logging

from campaigns.application.query import GetCampaignByIdQuery
from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_status import CampaignStatus
from products.application.command.delete_product.delete_product_command import (
    DeleteProductCommand,
)
from products.domain.exceptions.product_exception import ProductException
from products.domain.product import Product
from products.domain.repository.product_read_repository import ProductReadRepository
from products.domain.repository.product_write_repository import ProductWriteRepository
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.exceptions.not_found_exception import NotFoundException
from shared.domain.repository.campaign_file_storage import CampaignFileStorage


class DeleteProductCommandHandler(ICommandHandler[DeleteProductCommand]):
    """Handler for the DeleteProductCommand."""

    def __init__(
        self,
        query_bus: QueryBus,
        read_repository: ProductReadRepository,
        write_repository: ProductWriteRepository,
        campaign_file_storage: CampaignFileStorage,
    ):
        """
        :param query_bus: The query bus to use for querying the product's campaign.
        :param read_repository: The product repository to use for reading products.
        :param write_repository: The product repository to use for deleting products.
        :param campaign_file_storage: The storage used to delete the product's image.
        """
        self._query_bus = query_bus
        self._read_repository = read_repository
        self._write_repository = write_repository
        self._campaign_file_storage = campaign_file_storage
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: DeleteProductCommand) -> None:
        """
        Handle the DeleteProductCommand to delete a product by its ID.

        :param command: The command containing the product ID.
        :raises NotFoundException: If the product with the given ID does not exist.
        :raises ProductException: If the product's campaign isn't active.
        :raises Exception: If the product passed the checks above but still failed to delete.
        """
        self._logger.info(f"INIT :: Deleting product with ID: {command.product_id.str}")

        product = await self._read_repository.get_product_by_id(command.product_id)
        if product is None:
            raise NotFoundException.entity_not_found(Product.__name__, command.product_id.str)

        campaign: Campaign = await self._query_bus.query(GetCampaignByIdQuery(product.campaign_id))
        if campaign.status != CampaignStatus.ACTIVE:
            raise ProductException.campaign_not_active_to_delete(product.campaign_id.str)

        is_deleted = await self._write_repository.delete_product(command.product_id)
        if not is_deleted:
            raise Exception(f"Product with ID {command.product_id.str} could not be deleted.")

        file_name = product.image_url.str.rsplit("/", 1)[-1]
        self._campaign_file_storage.delete_file(product.campaign_id.str, file_name)
