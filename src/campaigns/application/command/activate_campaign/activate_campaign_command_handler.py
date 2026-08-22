import logging

from campaigns.application.command import ActivateCampaignCommand
from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_status import CampaignStatus
from campaigns.domain.exceptions.campaign_already_exists_exception import (
    CampaignAlreadyExistsException,
)
from campaigns.domain.repository.campaign_read_repository import CampaignReadRepository
from campaigns.domain.repository.campaign_write_repository import (
    CampaignWriteRepository,
)
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.exceptions.not_found_exception import NotFoundException


class ActivateCampaignCommandHandler(ICommandHandler[ActivateCampaignCommand]):
    """Handler for the ActivateCampaignCommand."""

    def __init__(
        self, read_repository: CampaignReadRepository, write_repository: CampaignWriteRepository
    ):
        """
        :param read_repository: The campaign repository to use for reading campaigns.
        :param write_repository: The campaign repository to use for activating campaigns.
        """
        self._read_repository = read_repository
        self._write_repository = write_repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: ActivateCampaignCommand) -> None:
        """
        Handle the ActivateCampaignCommand to activate a campaign.

        :param command: The command containing the campaign ID.
        :raises CampaignAlreadyExistsException: If another campaign is already active, or if
        this campaign is already active.
        :raises NotFoundException: If the campaign with the given ID does not exist.
        """
        self._logger.info(f"INIT :: Activating campaign with ID: {command.campaign_id.str}")

        if await self._read_repository.exists_active_campaign_excluding(command.campaign_id):
            raise CampaignAlreadyExistsException.active_campaign_already_exists()

        campaign = await self._read_repository.get_campaign_by_id(command.campaign_id)
        if campaign is None:
            raise NotFoundException.entity_not_found(Campaign.__name__, command.campaign_id.str)

        if campaign.status == CampaignStatus.ACTIVE:
            raise CampaignAlreadyExistsException.campaign_already_active(command.campaign_id.str)

        await self._write_repository.update_campaign_status(
            command.campaign_id, CampaignStatus.ACTIVE
        )
