import logging

from campaigns.application.command import FinishCampaignCommand
from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_status import CampaignStatus
from campaigns.domain.exceptions.campaign_cannot_be_finished_exception import (
    CampaignCannotBeFinishedException,
)
from campaigns.domain.repository.campaign_read_repository import CampaignReadRepository
from campaigns.domain.repository.campaign_write_repository import (
    CampaignWriteRepository,
)
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.exceptions.not_found_exception import NotFoundException


class FinishCampaignCommandHandler(ICommandHandler[FinishCampaignCommand]):
    """Handler for the FinishCampaignCommand."""

    def __init__(
        self, read_repository: CampaignReadRepository, write_repository: CampaignWriteRepository
    ):
        """
        :param read_repository: The campaign repository to use for reading campaigns.
        :param write_repository: The campaign repository to use for finishing campaigns.
        """
        self._read_repository = read_repository
        self._write_repository = write_repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: FinishCampaignCommand) -> None:
        """
        Handle the FinishCampaignCommand to finish a campaign.

        :param command: The command containing the campaign ID.
        :raises NotFoundException: If the campaign with the given ID does not exist.
        :raises CampaignCannotBeFinishedException: If the campaign's status is not ACTIVE.
        """
        self._logger.info(f"INIT :: Finishing campaign with ID: {command.campaign_id.str}")

        campaign = await self._read_repository.get_campaign_by_id(command.campaign_id)
        if campaign is None:
            raise NotFoundException.entity_not_found(Campaign.__name__, command.campaign_id.str)

        if campaign.status != CampaignStatus.ACTIVE:
            raise CampaignCannotBeFinishedException.status_not_finishable(campaign.status)

        await self._write_repository.update_campaign_status(
            command.campaign_id, CampaignStatus.FINISHED
        )
