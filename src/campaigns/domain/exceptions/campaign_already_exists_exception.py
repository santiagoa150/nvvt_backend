from typing import Any, Optional

from fastapi import status

from campaigns.domain.exceptions.campaign_exception_messages import (
    CampaignExceptionMessages,
)
from shared.domain.exceptions.common_exception import CommonException


class CampaignAlreadyExistsException(CommonException):
    """Exception raised when a campaign already exists."""

    def __init__(
        self,
        message: str,
        detail: Optional[Any] = None,
        error_code: Optional[str] = None,
    ):
        super().__init__(status.HTTP_409_CONFLICT, message, detail, error_code)

    @staticmethod
    def year_and_number_already_exists(year: int, number: int) -> "CampaignAlreadyExistsException":
        """Raises an exception when a campaign with the same year and number already exists."""
        return CampaignAlreadyExistsException(
            CampaignExceptionMessages.YEAR_AND_NUMBER_ALREADY_EXISTS.format(
                year=year, number=number
            ),
            detail={"year": year, "number": number},
            error_code="CAMPAIGN_YEAR_NUMBER_ALREADY_EXISTS",
        )

    @staticmethod
    def active_campaign_already_exists() -> "CampaignAlreadyExistsException":
        """Raises an exception when an active campaign already exists."""
        return CampaignAlreadyExistsException(
            CampaignExceptionMessages.ACTIVE_CAMPAIGN_ALREADY_EXISTS.format(),
            error_code="ACTIVE_CAMPAIGN_ALREADY_EXISTS",
        )
