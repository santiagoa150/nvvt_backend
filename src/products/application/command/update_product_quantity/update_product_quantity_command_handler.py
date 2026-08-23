import logging

from campaigns.application.query import GetCampaignByIdQuery
from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_status import CampaignStatus
from products.application.command.update_product_quantity.update_product_quantity_command import (
    UpdateProductQuantityCommand,
)
from products.domain.exceptions.product_exception import ProductException
from products.domain.product import Product
from products.domain.repository.product_read_repository import ProductReadRepository
from products.domain.repository.product_write_repository import ProductWriteRepository
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.exceptions.not_found_exception import NotFoundException


class UpdateProductQuantityCommandHandler(ICommandHandler[UpdateProductQuantityCommand]):
    """Handler for the UpdateProductQuantityCommand."""

    def __init__(
        self,
        query_bus: QueryBus,
        read_repository: ProductReadRepository,
        write_repository: ProductWriteRepository,
    ):
        """
        :param query_bus: The query bus to use for querying the product's campaign.
        :param read_repository: The product repository to use for reading products.
        :param write_repository: The product repository to use for updating products.
        """
        self._query_bus = query_bus
        self._read_repository = read_repository
        self._write_repository = write_repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: UpdateProductQuantityCommand) -> None:
        """
        Handle the UpdateProductQuantityCommand to update a product's quantity.

        :param command: The command containing the product ID and the new quantity.
        :raises NotFoundException: If the product with the given ID does not exist.
        :raises ProductException: If the product's campaign isn't active, or if the
            requested quantity matches the product's current one.
        """
        self._logger.info(
            f"INIT :: Updating quantity of product with ID: {command.product_id.str}"
        )

        product = await self._read_repository.get_product_by_id(command.product_id)
        if product is None:
            raise NotFoundException.entity_not_found(Product.__name__, command.product_id.str)

        campaign: Campaign = await self._query_bus.query(GetCampaignByIdQuery(product.campaign_id))
        if campaign.status != CampaignStatus.ACTIVE:
            raise ProductException.campaign_not_active_to_update(product.campaign_id.str)

        if product.quantity.int == command.quantity.int:
            raise ProductException.quantity_already_set(
                command.product_id.str, command.quantity.int
            )

        await self._write_repository.update_product_quantity(
            command.product_id, command.quantity
        )
