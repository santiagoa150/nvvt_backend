import logging

from receipts.application.command import (
    CreateClientReceiptCommand,
    CreateClientReceiptCommandResponse,
)
from receipts.domain.repository.receipt_generator import ReceiptGenerator
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.cqrs.query.query_bus import QueryBus


class CreateClientReceiptCommandHandler(ICommandHandler[CreateClientReceiptCommand]):
    """Handler for the CreateClientReceiptCommand."""

    def __init__(self, query_bus: QueryBus, receipt_generator: ReceiptGenerator):
        """
        :param query_bus: The query bus to use for querying campaigns, clients, orders and products.
        :param receipt_generator: The receipt generator to use for creating receipts.
        """
        self._query_bus = query_bus
        self._receipt_generator = receipt_generator
        self._logger = logging.getLogger(__name__)

    async def handle(
        self, command: CreateClientReceiptCommand
    ) -> CreateClientReceiptCommandResponse:
        """
        Handle the CreateClientReceiptCommand to create a new client receipt.
        :param command: The command containing the receipt details.
        """
        self._logger.info(
            f"INIT :: Generating receipt for Campaign and Client :: "
            f"{command.campaign_id.str}, {command.client_id.str}"
        )
        # Orders use cases were removed pending a refactor; re-wire this once they're rebuilt.
        raise NotImplementedError(
            "Receipt generation is disabled while the orders context is refactored."
        )
