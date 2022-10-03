from __future__ import annotations

import time

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

    def wait(self, task_id: int, timeout: int = 300) -> TaskStatus:
        """Wait for the specified task id

        Args:
            task_id (int): The celery task id
            timeout (int): The timeout in seconds

        Returns:
            TaskStatus: The task_status.

        Raises:
            TimeoutError: If the task does not complete within the timeout
        """
        for _ in range(timeout):
            status = self.get(task_id)
            if status.ready:
                return status
            time.sleep(1)
        raise TimeoutError(f"Timeout waiting for task {task_id}")
