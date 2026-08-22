from campaigns.domain.value_objects.campaign_number import CampaignNumber
from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.bool_value_object import BoolValueObject
from shared.domain.value_objects.common.year import Year
from shared.domain.value_objects.str_value_object import StringValueObject


class CreateCampaignCommand(ICommand):
    """Command to create a new campaign."""

    def __init__(
        self,
        name: StringValueObject,
        year: Year,
        number: CampaignNumber,
        is_active: BoolValueObject,
    ):
        """
        :param name: The name of the campaign.
        :param year: The year of the campaign.
        :param number: The number of the campaign.
        :param is_active: Whether the campaign should be marked as the active one.
        """
        self.name = name
        self.year = year
        self.number = number
        self.is_active = is_active

    @staticmethod
    def create(
        name: str,
        year: int,
        number: int,
        is_active: bool,
    ) -> "CreateCampaignCommand":
        """Factory method to create a CreateCampaignCommand instance."""
        return CreateCampaignCommand(
            name=StringValueObject(name, "campaign_name"),
            year=Year(year, "campaign_year"),
            number=CampaignNumber(number),
            is_active=BoolValueObject(is_active, "campaign_is_active"),
        )
