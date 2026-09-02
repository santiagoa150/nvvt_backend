from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.str_value_object import StringValueObject


class LoadCartCommand(ICommand):
    """Command to load every product from a provider's cart into a campaign."""

    def __init__(
        self,
        campaign_id: IdValueObject,
        provider_token: StringValueObject,
        cart_id: StringValueObject,
        requested_by: StringValueObject,
    ):
        """
        :param campaign_id: The ID of the campaign to load the cart into.
        :param provider_token: The bearer token used to authenticate against the provider.
        :param cart_id: The ID of the provider's cart to load.
        :param requested_by: The ID of the user who requested the cart to be loaded.
        """
        self.campaign_id = campaign_id
        self.provider_token = provider_token
        self.cart_id = cart_id
        self.requested_by = requested_by

    @staticmethod
    def create(
        campaign_id: str,
        provider_token: str,
        cart_id: str,
        requested_by: str,
    ) -> "LoadCartCommand":
        """Factory method to create a LoadCartCommand instance."""
        return LoadCartCommand(
            campaign_id=IdValueObject(campaign_id, "campaign_id"),
            provider_token=StringValueObject(provider_token, "provider_token"),
            cart_id=StringValueObject(cart_id, "cart_id"),
            requested_by=StringValueObject(requested_by, "requested_by"),
        )
