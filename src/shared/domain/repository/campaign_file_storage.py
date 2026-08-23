from abc import ABC, abstractmethod


class CampaignFileStorage(ABC):
    """Interface for managing campaign-scoped files served as static assets."""

    @abstractmethod
    def create_campaign_folder(self, campaign_id: str) -> None:
        """
        Create the storage folder for a campaign.

        :param campaign_id: The ID of the campaign.
        """
        pass

    @abstractmethod
    def delete_campaign_folder(self, campaign_id: str) -> None:
        """
        Delete the storage folder for a campaign, along with all its files.

        :param campaign_id: The ID of the campaign.
        """
        pass

    @abstractmethod
    def save_file(self, campaign_id: str, file_name: str, content: bytes) -> str:
        """
        Save a file inside the campaign's folder.

        :param campaign_id: The ID of the campaign the file belongs to.
        :param file_name: The name to store the file under.
        :param content: The raw file content.
        :return: The public path under which the file is now accessible.
        """
        pass

    @abstractmethod
    def delete_file(self, campaign_id: str, file_name: str) -> None:
        """
        Delete a file from the campaign's folder, if it exists.

        :param campaign_id: The ID of the campaign the file belongs to.
        :param file_name: The name of the file to delete.
        """
        pass
