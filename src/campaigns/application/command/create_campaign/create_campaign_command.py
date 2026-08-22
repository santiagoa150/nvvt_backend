from campaigns.domain.campaign_status import CampaignStatus
from campaigns.domain.value_objects.campaign_number import CampaignNumber
from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.common.year import Year
from shared.domain.value_objects.str_value_object import StringValueObject


class CreateCampaignCommand(ICommand):
    """Command to create a new campaign."""

    def __init__(
        self,
        name: StringValueObject,
        year: Year,
        number: CampaignNumber,
        status: CampaignStatus,
    ):
        """
        :param name: The name of the campaign.
        :param year: The year of the campaign.
        :param number: The number of the campaign.
        :param status: The status of the campaign.
        """
        self.name = name
        self.year = year
        self.number = number
        self.status = status

    @staticmethod
    def create(
        name: str,
        year: int,
        number: int,
        status: str,
    ) -> "CreateCampaignCommand":
        """Factory method to create a CreateCampaignCommand instance."""
        return CreateCampaignCommand(
            name=StringValueObject(name, "campaign_name"),
            year=Year(year, "campaign_year"),
            number=CampaignNumber(number),
            status=CampaignStatus.create(status),
        )
