from __future__ import annotations

from doccano_client.client import DoccanoClient
from doccano_client.models.task_status import TaskStatus


class TaskStatusRepository:
    """Repository for interacting with the Doccano task status API"""

    def __init__(self, client: DoccanoClient):
        self._client = client

    def get(self, task_id: int) -> TaskStatus:
        """Return the specified task_status

        Returns:
            TaskStatus: The task_status.
        """
        response = self._client.get(f"tasks/status/{task_id}")
        return TaskStatus.parse_obj(response.json())
