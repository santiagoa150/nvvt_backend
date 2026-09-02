from fastapi import status

from campaigns.domain.campaign_status import CampaignStatus
from campaigns.domain.exceptions.campaign_exception_messages import (
    CampaignExceptionMessages,
)
from shared.domain.exceptions.common_exception import CommonException


class CampaignCannotBeFinishedException(CommonException):
    """Exception raised when a campaign cannot be finished because of its status."""

    def __init__(self, message: str):
        super().__init__(
            status.HTTP_409_CONFLICT, message, error_code="CAMPAIGN_CANNOT_BE_FINISHED"
        )

    @staticmethod
    def status_not_finishable(
        campaign_status: CampaignStatus,
    ) -> "CampaignCannotBeFinishedException":
        """Raises an exception when a campaign's status does not allow finishing it."""
        return CampaignCannotBeFinishedException(
            CampaignExceptionMessages.CAMPAIGN_CANNOT_BE_FINISHED.format(
                campaign_status=campaign_status.value
            ),
        )
