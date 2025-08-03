from campaigns.domain.campaign import Campaign
from campaigns.domain.repository.campaign_repository import CampaignRepository
from shared.domain.value_objects.id_value_object import IdValueObject


class MongoDBCampaignRepository(CampaignRepository):
    def get_campaign_by_id(self, campaign_id: IdValueObject) -> Campaign | None:
        return Campaign.from_dict({
            "campaign_id": "425ed8c4-34d7-4766-b6eb-4021a21e4c00",
            "name": "Campaign Name",
            "year": 2025,
            "number": 1,
        })
