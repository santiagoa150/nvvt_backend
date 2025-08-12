from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject


class DeleteCampaignCommand(ICommand):
    """Command to delete a campaign by its ID."""

    def __init__(self, campaign_id: IdValueObject):
        """
        :param campaign_id: The ID of the campaign to delete.
        """
        self.campaign_id = campaign_id

    @staticmethod
    def create(campaign_id: str):
        """Factory method to create a DeleteCampaignCommand instance."""
        return DeleteCampaignCommand(campaign_id=IdValueObject(campaign_id, "campaign_id"))
