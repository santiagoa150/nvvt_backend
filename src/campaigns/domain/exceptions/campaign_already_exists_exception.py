from fastapi import status

from campaigns.domain.exceptions.campaign_exception_messages import CampaignExceptionMessages
from shared.domain.exceptions.common_exception import CommonException


class CampaignAlreadyExistsException(CommonException):
    """Exception raised when a campaign already exists."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_409_CONFLICT, message)

    @staticmethod
    def year_and_number_already_exists(year: int, number: int) -> "CampaignAlreadyExistsException":
        """Raises an exception when a campaign with the same year and number already exists."""
        return CampaignAlreadyExistsException(
            CampaignExceptionMessages.YEAR_AND_NUMBER_ALREADY_EXISTS.format(year=year, number=number)
        )
