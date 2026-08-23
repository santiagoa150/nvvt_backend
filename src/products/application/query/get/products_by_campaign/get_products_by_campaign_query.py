from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.value_objects.id_value_object import IdValueObject


class GetProductsByCampaignQuery(IQuery):
    """Query to get all products belonging to a campaign."""

    def __init__(self, campaign_id: IdValueObject):
        """
        :param campaign_id: The ID of the campaign to retrieve products for.
        """
        self.campaign_id = campaign_id

    @staticmethod
    def create(campaign_id: str) -> "GetProductsByCampaignQuery":
        """Factory method to create a GetProductsByCampaignQuery instance."""
        return GetProductsByCampaignQuery(campaign_id=IdValueObject(campaign_id, "campaign_id"))
