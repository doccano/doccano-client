from unittest.mock import MagicMock

from doccano_client.usecase.data_upload import DataUploadUseCase


class TestDataUploadUseCase:
    @classmethod
    def setup_method(cls):
        cls.data_upload_repository = MagicMock()
        cls.task_status_repository = MagicMock()
        cls.usecase = DataUploadUseCase(cls.data_upload_repository, cls.task_status_repository)

    def test_list(self):
        self.usecase.list_options(0)
        self.data_upload_repository.list_options.assert_called_once_with(0)

    def test_upload(self):
        project_id = 0
        self.data_upload_repository.upload.return_value = "upload_id"
        self.usecase.upload(
            project_id,
            file_paths=["test.txt"],
            task="DocumentClassification",
            format="JSONL",
            column_data="text",
            column_label="label",
        )
        self.data_upload_repository.upload.assert_called_once_with("test.txt")
        self.data_upload_repository.ingest.assert_called_once_with(
            project_id, ["upload_id"], "DocumentClassification", "JSONL", column_data="text", column_label="label"
        )
