from fastapi import status

from campaigns.domain.exceptions.campaign_exception_messages import CampaignExceptionMessages
from shared.domain.exceptions.common_exception import CommonException


class CampaignStatusException(CommonException):
    """Exception raised when there is an issue with the campaign status."""

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code, message)

    @staticmethod
    def invalid_campaign_status(value: str) -> "CampaignStatusException":
        """Raises an exception when the campaign status is invalid."""
        return CampaignStatusException(
            CampaignExceptionMessages.INVALID_CAMPAIGN_STATUS.format(campaign_status=value),
        )
