from io import BytesIO
from typing import TypedDict

from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject


class CreateClientReceiptCommand(ICommand):

    def __init__(
            self,
            campaign_id: IdValueObject,
            client_id: IdValueObject,
    ):
        """
        :param campaign_id: The ID of the campaign associated with the receipt.
        :param client_id: The ID of the client for whom the receipt is created.
        """
        self.campaign_id = campaign_id
        self.client_id = client_id

    @staticmethod
    def create(
            campaign_id: str,
            client_id: str,
    ) -> "CreateClientReceiptCommand":
        """Factory method to create a CreateClientReceiptCommand instance."""
        return CreateClientReceiptCommand(
            campaign_id=IdValueObject(campaign_id, 'campaign_id'),
            client_id=IdValueObject(client_id, 'client_id'),
        )

class CreateClientReceiptCommandResponse(TypedDict):
    """Response type for CreateClientReceiptCommandHandler."""
    receipt: BytesIO
    title: str
