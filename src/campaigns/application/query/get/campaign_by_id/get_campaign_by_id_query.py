from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.value_objects.id_value_object import IdValueObject


class GetCampaignByIdQuery(IQuery):
    """Query to get a campaign by its ID."""

    def __init__(self, campaign_id: IdValueObject):
        """
        :param campaign_id: The ID of the campaign to retrieve.
        """
        self.campaign_id = campaign_id

    @staticmethod
    def create(campaign_id: str):
        """Factory method to create a GetCampaignByIdQuery instance."""
        return GetCampaignByIdQuery(campaign_id=IdValueObject(campaign_id, "campaign_id"))
