from unittest.mock import MagicMock

from doccano_client.models.data_export import Option
from doccano_client.usecase.data_export import DataExportUseCase


class TestDataExportUseCase:
    @classmethod
    def setup_method(cls):
        cls.data_export_repository = MagicMock()
        cls.task_status_repository = MagicMock()
        cls.usecase = DataExportUseCase(cls.data_export_repository, cls.task_status_repository)

    def test_list(self):
        self.usecase.list_options(0)
        self.data_export_repository.list_options.assert_called_once_with(0)

    def test_download(self):
        project_id = 0
        task_id = "task_id"
        option = Option(name="test", format="JSONL")
        self.data_export_repository.schedule_download.return_value = task_id
        self.data_export_repository.find_option_by_name.return_value = option
        self.usecase.download(project_id, "JSONL", only_approved=True, dir_name=".")
        self.data_export_repository.schedule_download.assert_called_once_with(project_id, option, True)
        self.task_status_repository.wait.assert_called_once_with(task_id)
        self.data_export_repository.download.assert_called_once_with(project_id, task_id, ".")
