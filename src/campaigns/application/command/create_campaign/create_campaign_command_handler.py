import logging

from campaigns.application.command import CreateCampaignCommand
from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_dict import CampaignDict
from campaigns.domain.campaign_status import CampaignStatus
from campaigns.domain.exceptions.campaign_already_exists_exception import (
    CampaignAlreadyExistsException,
)
from campaigns.domain.repository.campaign_read_repository import CampaignReadRepository
from campaigns.domain.repository.campaign_write_repository import (
    CampaignWriteRepository,
)
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.repository.campaign_file_storage import CampaignFileStorage
from shared.domain.value_objects.id_value_object import IdValueObject


class CreateCampaignCommandHandler(ICommandHandler[CreateCampaignCommand]):
    """Handler for the CreateCampaignCommand."""

    def __init__(
        self,
        read_repository: CampaignReadRepository,
        write_repository: CampaignWriteRepository,
        file_storage: CampaignFileStorage,
    ):
        """
        :param write_repository: The campaign repository to use for creating campaigns.
        :param file_storage: The storage used to create the campaign's file folder.
        """
        self._read_repository = read_repository
        self._write_repository = write_repository
        self._file_storage = file_storage
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: CreateCampaignCommand) -> None:
        """
        Handle the CreateCampaignCommand to create a new campaign.
        :param command: The command containing the campaign details.
        :raises CampaignAlreadyExistsException: If a campaign with the same year and number
        already exists, or if the command marks the campaign as active while another active
        campaign already exists.
        """
        self._logger.info(
            f"INIT :: Creating Campaign with params: "
            f"{command.year}, {command.number}, {command.name}, {command.status}"
        )

        if await self._read_repository.exists_by_year_and_number(command.year, command.number):
            raise CampaignAlreadyExistsException.year_and_number_already_exists(
                command.year.int, command.number.int
            )

        if (
            command.status == CampaignStatus.ACTIVE
            and await self._read_repository.exists_active_campaign()
        ):
            raise CampaignAlreadyExistsException.active_campaign_already_exists()

        campaign_id = IdValueObject.generate()
        campaign = Campaign.from_dict(
            CampaignDict(
                campaign_id=campaign_id,
                name=command.name.str,
                year=command.year.int,
                number=command.number.int,
                status=command.status.value,
            )
        )
        await self._write_repository.create_campaign(campaign)
        self._file_storage.create_campaign_folder(campaign_id)
