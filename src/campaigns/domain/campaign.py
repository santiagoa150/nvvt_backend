from campaigns.domain.campaign_dict import CampaignDict
from campaigns.domain.value_objects.campaign_number import CampaignNumber
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.string_value_object import StringValueObject
from shared.domain.value_objects.common.year import Year


class Campaign:
    """Represents a campaign with its associated properties."""

    def __init__(
            self,
            campaign_id: IdValueObject,
            name: StringValueObject,
            year: Year,
            number: CampaignNumber,
    ):
        self._campaign_id = campaign_id
        self._name = name
        self._year = year
        self._number = number

    def to_dict(self) -> CampaignDict:
        """Converts the campaign to a dictionary representation."""
        return CampaignDict(
            campaign_id=self._campaign_id.str,
            name=self._name.str,
            year=self._year.int,
            number=self._number.int,
        )

    @classmethod
    def from_dict(cls, campaign_dict: CampaignDict) -> "Campaign":
        """Creates a Campaign instance from a dictionary representation."""
        return cls(
            campaign_id=IdValueObject(campaign_dict["campaign_id"]),
            name=StringValueObject(campaign_dict["name"]),
            year=Year(campaign_dict["year"]),
            number=CampaignNumber(campaign_dict["number"]),
        )
