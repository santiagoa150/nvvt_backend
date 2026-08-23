import os
import shutil

from shared.domain.repository.campaign_file_storage import CampaignFileStorage


class LocalCampaignFileStorage(CampaignFileStorage):
    """Local filesystem implementation of CampaignFileStorage."""

    def __init__(self, base_path: str, url_prefix: str):
        """
        :param base_path: The local directory campaign folders are created under.
        :param url_prefix: The URL prefix under which base_path is served as static files.
        """
        self._base_path = base_path
        self._url_prefix = url_prefix.rstrip("/")
        os.makedirs(self._base_path, exist_ok=True)

    def _campaign_folder_path(self, campaign_id: str) -> str:
        return os.path.join(self._base_path, campaign_id)

    def create_campaign_folder(self, campaign_id: str) -> None:
        """Creates the storage folder for a campaign."""
        os.makedirs(self._campaign_folder_path(campaign_id), exist_ok=True)

    def delete_campaign_folder(self, campaign_id: str) -> None:
        """Deletes the storage folder for a campaign, along with all its files."""
        folder_path = self._campaign_folder_path(campaign_id)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)

    def save_file(self, campaign_id: str, file_name: str, content: bytes) -> str:
        """Saves a file inside the campaign's folder and returns its public path."""
        folder_path = self._campaign_folder_path(campaign_id)
        os.makedirs(folder_path, exist_ok=True)

        with open(os.path.join(folder_path, file_name), "wb") as file:
            file.write(content)

        return f"{self._url_prefix}/{campaign_id}/{file_name}"
