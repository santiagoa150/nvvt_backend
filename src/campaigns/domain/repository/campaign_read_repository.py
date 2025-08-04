from abc import ABC, abstractmethod
from typing import Optional

from campaigns.domain.campaign import Campaign
from campaigns.domain.value_objects.campaign_number import CampaignNumber
from shared.domain.pagination_dict import PaginationDict
from shared.domain.value_objects.common.year import Year
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam


class CampaignReadRepository(ABC):
    """Abstract base class for campaign reading repository operations."""

    @abstractmethod
    async def get_campaign_by_id(self, campaign_id: IdValueObject) -> Optional[Campaign]:
        """
        Retrieve a campaign by its ID.

        :param campaign_id: The ID of the campaign to retrieve.
        :return: An instance of Campaign if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_paginated_campaigns(self, page: PageParam, limit: LimitParam) -> PaginationDict[Campaign]:
        """
        Retrieve paginated campaigns.

        :param page: The page number to retrieve.
        :param limit: The number of items per page.
        :return: A PaginationDict containing the paginated campaigns.
        """
        pass

    @abstractmethod
    async def exists_by_year_and_number(self, year: Year, number: CampaignNumber) -> bool:
        """
        Check if a campaign exists by year and number.

        :param year: The year of the campaign.
        :param number: The number of the campaign.
        :return: True if a campaign exists with the specified year and number, otherwise False.
        """
        pass
