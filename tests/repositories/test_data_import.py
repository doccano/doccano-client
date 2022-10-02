import pathlib

import vcr

from doccano_client.models.data_import import Option
from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.data_import import DataImportRepository
from tests.conftest import cassettes_path


class TestDataImportRepository:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(cassettes_path / "data_import/login.yaml"), mode="once"):
            client = BaseRepository("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = DataImportRepository(client)
        cls.project_id = 16
        cls.file_path = pathlib.Path(__file__).parent / "data/classification.json"

    def test_list_options(self):
        with vcr.use_cassette(str(cassettes_path / "data_import/options.yaml"), mode="once"):
            response = self.client.list_options(self.project_id)
        assert len(response) > 0
        assert all(isinstance(option, Option) for option in response)

    def test_upload(self):
        with vcr.use_cassette(str(cassettes_path / "data_import/upload.yaml"), mode="once"):
            upload_id = self.client.upload(self.file_path)
        assert upload_id is not None
        assert isinstance(upload_id, str)

    def test_delete(self):
        with vcr.use_cassette(str(cassettes_path / "data_import/delete.yaml"), mode="once"):
            upload_id = self.client.upload(self.file_path)
            self.client.delete(upload_id)

    def test_ingest(self):
        with vcr.use_cassette(str(cassettes_path / "data_import/ingest.yaml"), mode="once"):
            upload_id = self.client.upload(self.file_path)
            task_id = self.client.ingest(self.project_id, [upload_id], task="DocumentClassification", format="JSONL")
        assert task_id is not None
        assert isinstance(task_id, str)
