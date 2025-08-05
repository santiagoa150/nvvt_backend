from orders.domain.order_provider import OrderProvider
from orders.domain.order_provider_dict import OrderProviderDict
from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject
from shared.domain.value_objects.string_value_object import StringValueObject


class CreateOrderCommand(ICommand):
    """Command to create a new order."""

    def __init__(
            self,
            provider: OrderProvider,
            product_url: StringValueObject,
            campaign_id: IdValueObject,
            client_id: IdValueObject,
            quantity: PositiveIntValueObject,
    ):
        """
        :param provider: The order provider associated with the order.
        :param product_url: The URL of the product to order.
        :param client_id: The ID of the client placing the order.
        :param quantity: The quantity of the item to order.
        """
        self.provider = provider
        self.product_url = product_url
        self.campaign_id = campaign_id
        self.client_id = client_id
        self.quantity = quantity

    @staticmethod
    def create(
            session_id: str,
            route: str,
            accelerator_secure_guid: str,
            cebs_p: str,
            cebs: str,
            product_url: str,
            campaign_id: str,
            client_id: str,
            quantity: int,
    ) -> "CreateOrderCommand":
        """Factory method to create a CreateOrderCommand instance."""
        return CreateOrderCommand(
            provider=OrderProvider.from_dict(OrderProviderDict(
                session_id=session_id,
                route=route,
                accelerator_secure_guid=accelerator_secure_guid,
                cebs_p=cebs_p,
                cebs=cebs
            )),
            product_url=StringValueObject(product_url, 'product_url'),
            campaign_id=IdValueObject(campaign_id, 'campaign_id'),
            client_id=IdValueObject(client_id, 'client_id'),
            quantity=PositiveIntValueObject(quantity, 'order_quantity')
        )
