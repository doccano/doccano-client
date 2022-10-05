from unittest.mock import MagicMock

from doccano_client.usecase.data_import import DataImportUseCase


class TestDataImportUseCase:
    @classmethod
    def setup_method(cls):
        cls.data_import_repository = MagicMock()
        cls.task_status_repository = MagicMock()
        cls.usecase = DataImportUseCase(cls.data_import_repository, cls.task_status_repository)

    def test_list(self):
        self.usecase.list_options(0)
        self.data_import_repository.list_options.assert_called_once_with(0)

    def test_upload(self):
        project_id = 0
        self.data_import_repository.upload.return_value = "upload_id"
        self.usecase.upload(
            project_id,
            file_paths=["test.txt"],
            task="DocumentClassification",
            format="JSONL",
            column_data="text",
            column_label="label",
        )
        self.data_import_repository.upload.assert_called_once_with("test.txt")
        self.data_import_repository.ingest.assert_called_once_with(
            project_id, ["upload_id"], "DocumentClassification", "JSONL", column_data="text", column_label="label"
        )
