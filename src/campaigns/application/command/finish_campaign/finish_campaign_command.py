from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject


class FinishCampaignCommand(ICommand):
    """Command to finish a campaign."""

    def __init__(self, campaign_id: IdValueObject):
        """
        :param campaign_id: The ID of the campaign to finish.
        """
        self.campaign_id = campaign_id

    @staticmethod
    def create(campaign_id: str) -> "FinishCampaignCommand":
        """Factory method to create a FinishCampaignCommand instance."""
        return FinishCampaignCommand(campaign_id=IdValueObject(campaign_id, "campaign_id"))
