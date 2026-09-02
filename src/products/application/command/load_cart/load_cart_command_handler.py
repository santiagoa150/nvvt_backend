import logging

from notifications.application.command import SendNotificationCommand
from products.application.command.create_product.create_product_command import (
    CreateProductCommand,
)
from products.application.command.load_cart.load_cart_command import LoadCartCommand
from products.domain.product_provider import ProductProvider
from products.domain.repository.product_client import ProductClient
from shared.domain.cqrs.command.command_bus import CommandBus
from shared.domain.cqrs.command.icommand_handler import ICommandHandler

_CART_LOADED_ACTION = "CART_LOADED"
_CART_LOAD_FAILED_ACTION = "CART_LOAD_FAILED"


class LoadCartCommandHandler(ICommandHandler[LoadCartCommand]):
    """Handler for the LoadCartCommand."""

    def __init__(self, command_bus: CommandBus, product_client: ProductClient):
        """
        :param command_bus: The command bus used to create each product and notify the user.
        :param product_client: The client used to fetch the provider's cart.
        """
        self._command_bus = command_bus
        self._product_client = product_client
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: LoadCartCommand) -> None:
        """
        Handle the LoadCartCommand by fetching the provider's cart and creating a
        product for every item in it, then notifying the requesting user.

        A product that fails to be created (e.g. it already exists in the
        campaign) is logged as a warning and skipped, without interrupting the
        rest of the cart.
        """
        self._logger.info(
            f"INIT :: Loading cart {command.cart_id.str} into campaign {command.campaign_id.str}"
        )

        try:
            provider = ProductProvider(provider_token=command.provider_token, cart_id=command.cart_id)
            cart_items = await self._product_client.get_cart_items(provider, command.cart_id)

            for item in cart_items:
                try:
                    await self._command_bus.dispatch(
                        CreateProductCommand.create(
                            provider_token=command.provider_token.str,
                            code=item.code.str,
                            quantity=item.quantity.int,
                            campaign_id=command.campaign_id.str,
                        )
                    )
                except Exception as error:
                    self._logger.warning(
                        f"Could not create product with code {item.code.str} for campaign "
                        f"{command.campaign_id.str}: {error}"
                    )

            action = _CART_LOADED_ACTION
            self._logger.info(
                f"DONE :: Finished loading cart {command.cart_id.str} into campaign "
                f"{command.campaign_id.str}"
            )
        except Exception as error:
            self._logger.error(
                f"Failed to load cart {command.cart_id.str} into campaign "
                f"{command.campaign_id.str}: {error}"
            )
            action = _CART_LOAD_FAILED_ACTION

        await self._command_bus.dispatch(
            SendNotificationCommand.create(action=action, recipient=command.requested_by.str)
        )
