import pathlib
from typing import List

from doccano_client.models.data_download import Option
from doccano_client.repositories.data_download import DataDownloadRepository
from doccano_client.repositories.task_status import TaskStatusRepository


class DataDownloadUseCase:
    def __init__(self, data_download_repository: DataDownloadRepository, task_status_repository: TaskStatusRepository):
        self._data_download_repository = data_download_repository
        self._task_status_repository = task_status_repository

    def list_options(self, project_id: int) -> List[Option]:
        """Return all download options

        Args:
            project_id (int): The id of the project

        Returns:
            List[Option]: The list of the download options.
        """
        return self._data_download_repository.list_options(project_id)

    def download(self, project_id: int, format: str, only_approved=False, dir_name=".") -> pathlib.Path:
        """Download a file

        Args:
            project_id (int): The id of the project
            format (str): The format of the download
            only_approved (bool): Whether to download approved data only
            dir_name (str): The directory to save the file

        Returns:
            pathlib.Path: The path to the downloaded file
        """
        option = self._data_download_repository.find_option_by_name(project_id, format)
        task_id = self._data_download_repository.schedule_download(project_id, option, only_approved)
        self._task_status_repository.wait(task_id)
        file_path = self._data_download_repository.download(project_id, task_id, dir_name)
        return file_path
