from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.value_objects.id_value_object import IdValueObject


class GetOrdersByCampaignQuery(IQuery):
    """Query to get orders by campaign ID."""

    def __init__(self, campaign_id: IdValueObject):
        """
        :param campaign_id: The ID of the campaign to retrieve orders for.
        """
        self.campaign_id = campaign_id

    @staticmethod
    def create(campaign_id: str):
        """Factory method to create a GetOrdersByCampaignQuery instance."""
        return GetOrdersByCampaignQuery(
            IdValueObject(campaign_id, "campaign_id")
        )
