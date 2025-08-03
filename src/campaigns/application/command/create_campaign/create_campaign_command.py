from campaigns.domain.value_objects.campaign_number import CampaignNumber
from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.common.year import Year
from shared.domain.value_objects.string_value_object import StringValueObject


class CreateCampaignCommand(ICommand):
    """Command to create a new campaign."""

    def __init__(
            self,
            name: StringValueObject,
            year: Year,
            number: CampaignNumber,
    ):
        """
        :param name: The name of the campaign.
        :param year: The year of the campaign.
        :param number: The number of the campaign.
        """
        self.name = name
        self.year = year
        self.number = number
