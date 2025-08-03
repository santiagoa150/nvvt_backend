from campaigns.application.command.delete_campaign.delete_campaign_command import DeleteCampaignCommand
from campaigns.domain.campaign import Campaign
from campaigns.domain.repository.campaign_write_repository import CampaignWriteRepository
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.exceptions.not_found_exception import NotFoundException


class DeleteCampaignCommandHandler(ICommandHandler[DeleteCampaignCommand]):
    """Handler for the DeleteCampaignCommand."""

    def __init__(self, repository: CampaignWriteRepository):
        """
        :param repository: The campaign repository to use for deleting campaigns.
        """
        self._repository = repository

    async def handle(self, command: DeleteCampaignCommand) -> None:
        """
        Handle the DeleteCampaignCommand to delete a campaign by its ID.
        :param command: The command containing the campaign ID.
        """
        is_deleted = await self._repository.delete_campaign(command.campaign_id)
        if not is_deleted:
            raise NotFoundException.entity_not_found(Campaign.__name__, command.campaign_id.str)
