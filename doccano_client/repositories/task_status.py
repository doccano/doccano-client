from __future__ import annotations

from doccano_client.models.task_status import TaskStatus
from doccano_client.repositories.base import BaseRepository


class TaskStatusRepository:
    """Repository for interacting with the Doccano task status API"""

    def __init__(self, client: BaseRepository):
        self._client = client

    def get(self, task_id: int) -> TaskStatus:
        """Return the specified task_status

        Args:
            task_id (int): The celery task id

        Returns:
            TaskStatus: The task_status.
        """
        response = self._client.get(f"tasks/status/{task_id}")
        return TaskStatus.parse_obj(response.json())
