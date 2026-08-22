from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject


class ActivateCampaignCommand(ICommand):
    """Command to activate a campaign."""

    def __init__(self, campaign_id: IdValueObject):
        """
        :param campaign_id: The ID of the campaign to activate.
        """
        self.campaign_id = campaign_id

    @staticmethod
    def create(campaign_id: str) -> "ActivateCampaignCommand":
        """Factory method to create an ActivateCampaignCommand instance."""
        return ActivateCampaignCommand(campaign_id=IdValueObject(campaign_id, "campaign_id"))
