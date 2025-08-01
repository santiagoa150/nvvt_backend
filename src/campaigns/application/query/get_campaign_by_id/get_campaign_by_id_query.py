from shared.infrastructure.cqrs.query.iquery import IQuery


class GetCampaignByIdQuery(IQuery):
    """Query to get a campaign by its ID."""

    def __init__(self, campaign_id: str):
        """
        :param campaign_id: The ID of the campaign to retrieve.
        """
        self.campaign_id = campaign_id
