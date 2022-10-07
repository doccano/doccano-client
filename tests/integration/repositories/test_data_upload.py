import pathlib

import vcr

from doccano_client.models.data_upload import Option
from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.data_upload import DataUploadRepository
from tests.conftest import repository_fixtures


class TestDataUploadRepository:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(repository_fixtures / "data_upload/login.yaml"), mode="once"):
            client = BaseRepository("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = DataUploadRepository(client)
        cls.project_id = 16
        cls.file_path = pathlib.Path(__file__).parent.parent / "data/classification.jsonl"

    def test_list_options(self):
        with vcr.use_cassette(str(repository_fixtures / "data_upload/options.yaml"), mode="once"):
            response = self.client.list_options(self.project_id)
        assert len(response) > 0
        assert all(isinstance(option, Option) for option in response)

    def test_upload(self):
        with vcr.use_cassette(str(repository_fixtures / "data_upload/upload.yaml"), mode="once"):
            upload_id = self.client.upload(self.file_path)
        assert upload_id is not None
        assert isinstance(upload_id, str)

    def test_delete(self):
        with vcr.use_cassette(str(repository_fixtures / "data_upload/delete.yaml"), mode="once"):
            upload_id = self.client.upload(self.file_path)
            self.client.delete(upload_id)

    def test_ingest(self):
        with vcr.use_cassette(str(repository_fixtures / "data_upload/ingest.yaml"), mode="once"):
            upload_id = self.client.upload(self.file_path)
            task_id = self.client.ingest(self.project_id, [upload_id], task="DocumentClassification", format="JSONL")
        assert task_id is not None
        assert isinstance(task_id, str)
