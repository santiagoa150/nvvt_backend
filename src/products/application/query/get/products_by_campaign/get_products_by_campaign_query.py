from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.value_objects.id_value_object import IdValueObject


class GetProductsByCampaignQuery(IQuery):
    """Query to get all products belonging to a campaign."""

    def __init__(self, campaign_id: IdValueObject):
        """
        :param campaign_id: The ID of the campaign to retrieve products for.
        """
        self.campaign_id = campaign_id
