from __future__ import annotations

import pathlib
from typing import List

from doccano_client.models.data_download import Option
from doccano_client.repositories.base import BaseRepository


class DataDownloadRepository:
    """Repository for interacting with the Doccano data download API"""

    def __init__(self, client: BaseRepository):
        self._client = client

    def list_options(self, project_id: int) -> List[Option]:
        """Return all download options

        Args:
            project_id (int): The id of the project

        Returns:
            List[Option]: The list of the download options.
        """
        resource = f"projects/{project_id}/download-format"
        response = self._client.get(resource)
        options = [Option.parse_obj(label) for label in response.json()]
        return options

    def find_option_by_name(self, project_id: int, name: str) -> Option:
        """Find a download option by name

        Args:
            project_id (int): The id of the project
            name (str): The name of the download option to find

        Returns:
            Option: The found download option

        Raises:
            ValueError: If the download option is not found
        """
        options = self.list_options(project_id)
        for option in options:
            if option.name == name:
                return option
        raise ValueError(f"Download option '{name}' not found")

    def schedule_download(self, project_id: int, option: Option, only_approved=False) -> str:
        """Schedule a download

        Args:
            project_id (int): The id of the project
            option (Option): The download option
            only_approved (bool): Whether to download approved data only

        Returns:
            str: The celery task id
        """
        resource = f"projects/{project_id}/download"
        data = {"format": option.name, "exportApproved": only_approved}
        response = self._client.post(resource, json=data)
        task_id = response.json()["task_id"]
        return task_id

    def download(self, project_id: int, task_id: str, dir_name=".") -> pathlib.Path:
        """Download a file from the server

        Args:
            project_id (int): The id of the project
            task_id (str): The celery task id
            dir_name (str): The directory to save the file

        Returns:
            pathlib.Path: The path to the downloaded file
        """
        resource = f"projects/{project_id}/download"
        params = {"taskId": task_id}
        response = self._client.get(resource, params=params, stream=True)
        content_disposition = response.headers["Content-Disposition"]
        ATTRIBUTE = "filename="
        file_name = content_disposition[content_disposition.find(ATTRIBUTE) + len(ATTRIBUTE) + 1 : -1]
        dir_path = pathlib.Path(dir_name)
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / file_name
        with file_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return file_path
