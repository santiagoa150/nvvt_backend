import logging

from campaigns.application.command import DeleteCampaignCommand
from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_status import CampaignStatus
from campaigns.domain.exceptions.campaign_cannot_be_deleted_exception import (
    CampaignCannotBeDeletedException,
)
from campaigns.domain.repository.campaign_read_repository import CampaignReadRepository
from campaigns.domain.repository.campaign_write_repository import (
    CampaignWriteRepository,
)
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.exceptions.not_found_exception import NotFoundException


class DeleteCampaignCommandHandler(ICommandHandler[DeleteCampaignCommand]):
    """Handler for the DeleteCampaignCommand."""

    def __init__(
        self, read_repository: CampaignReadRepository, write_repository: CampaignWriteRepository
    ):
        """
        :param read_repository: The campaign repository to use for reading campaigns.
        :param write_repository: The campaign repository to use for deleting campaigns.
        """
        self._read_repository = read_repository
        self._write_repository = write_repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: DeleteCampaignCommand) -> None:
        """
        Handle the DeleteCampaignCommand to delete a campaign by its ID.
        :param command: The command containing the campaign ID.
        :raises NotFoundException: If the campaign with the given ID does not exist.
        :raises CampaignCannotBeDeletedException: If the campaign's status is not SCHEDULED.
        :raises Exception: If the campaign passed the checks above but still failed to delete.
        """
        self._logger.info(f"INIT :: Deleting campaign with ID: {command.campaign_id.str}")

        campaign = await self._read_repository.get_campaign_by_id(command.campaign_id)
        if campaign is None:
            raise NotFoundException.entity_not_found(Campaign.__name__, command.campaign_id.str)

        if campaign.status != CampaignStatus.SCHEDULED:
            raise CampaignCannotBeDeletedException.status_not_deletable(campaign.status)

        is_deleted = await self._write_repository.delete_campaign(command.campaign_id)
        if not is_deleted:
            raise Exception(f"Campaign with ID {command.campaign_id.str} could not be deleted.")
