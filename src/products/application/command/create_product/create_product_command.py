from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject
from shared.domain.value_objects.str_value_object import StringValueObject


class CreateProductCommand(ICommand):
    """Command to create a new product for a campaign."""

    def __init__(
        self,
        provider_token: StringValueObject,
        code: StringValueObject,
        quantity: PositiveIntValueObject,
        campaign_id: IdValueObject,
    ):
        """
        :param provider_token: The bearer token used to authenticate against the provider.
        :param code: The code of the product to create.
        :param quantity: The quantity of the product.
        :param campaign_id: The ID of the campaign the product belongs to.
        """
        self.provider_token = provider_token
        self.code = code
        self.quantity = quantity
        self.campaign_id = campaign_id

    @staticmethod
    def create(
        provider_token: str,
        code: str,
        quantity: int,
        campaign_id: str,
    ) -> "CreateProductCommand":
        """Factory method to create a CreateProductCommand instance."""
        return CreateProductCommand(
            provider_token=StringValueObject(provider_token, "provider_token"),
            code=StringValueObject(code, "product_code"),
            quantity=PositiveIntValueObject(quantity, "product_quantity"),
            campaign_id=IdValueObject(campaign_id, "campaign_id"),
        )
