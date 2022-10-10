from typing import List

from doccano_client.models.data_upload import Option, Task
from doccano_client.models.task_status import TaskStatus
from doccano_client.repositories.data_upload import DataUploadRepository
from doccano_client.repositories.task_status import TaskStatusRepository


class DataUploadUseCase:
    def __init__(self, data_upload_repository: DataUploadRepository, task_status_repository: TaskStatusRepository):
        self._data_upload_repository = data_upload_repository
        self._task_status_repository = task_status_repository

    def list_options(self, project_id: int) -> List[Option]:
        """Return all upload options

        Args:
            project_id (int): The id of the project

        Returns:
            List[Option]: The list of the upload options.
        """
        return self._data_upload_repository.list_options(project_id)

    def upload(
        self,
        project_id: int,
        file_paths: List[str],
        task: Task,
        format: str,
        column_data: str = "text",
        column_label: str = "label",
    ) -> TaskStatus:
        """Upload a file

        Args:
            project_id (int): The id of the project
            file_paths (List[str]): The list of the file paths
            task (Task): The task of the upload
            format (str): The format of the upload
            column_data (str): The column name of the data
            column_label (str): The column name of the label

        Returns:
            TaskStatus: The status of the upload task.
        """
        upload_ids = [self._data_upload_repository.upload(file_path) for file_path in file_paths]
        task_id = self._data_upload_repository.ingest(
            project_id, upload_ids, task, format, column_data=column_data, column_label=column_label
        )
        return self._task_status_repository.wait(task_id)
