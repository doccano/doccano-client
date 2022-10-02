from __future__ import annotations

from typing import Any, Iterator, List

from doccano_client.client import DoccanoClient
from doccano_client.models.data_export import Option


class DataExportClient:
    """Client for interacting with the Doccano data export API"""

    def __init__(self, client: DoccanoClient):
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

    def schedule_download(self, project_id: int, option: Option, only_approved=False) -> str:
        """Schedule a download

        Args:
            project_id (int): The id of the project
            option (Option): The download option
            only_approved (bool): Whether to export approved data only

        Returns:
            str: The celery task id
        """
        resource = f"projects/{project_id}/download"
        data = {"format": option.name, "exportApproved": only_approved}
        response = self._client.post(resource, json=data)
        task_id = response.json()["task_id"]
        return task_id

    def download(self, project_id: int, task_id: str) -> Iterator[Any]:
        """Download a file from the server

        Args:
            project_id (int): The id of the project
            task_id (str): The celery task id

        Yields:
            Iterator[Any]: The file content
        """
        resource = f"projects/{project_id}/download"
        params = {"taskId": task_id}
        response = self._client.get(resource, params=params, stream=True)
        yield from response.iter_content(chunk_size=65536)
