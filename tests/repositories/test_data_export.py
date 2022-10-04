import pathlib
import time

import vcr

from doccano_client.models.data_export import Option
from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.data_export import DataExportRepository
from tests.conftest import cassettes_path


class TestDataExportRepository:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(cassettes_path / "data_export/login.yaml"), mode="once"):
            client = BaseRepository("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = DataExportRepository(client)
        cls.project_id = 16

    def test_list_options(self):
        with vcr.use_cassette(str(cassettes_path / "data_export/options.yaml"), mode="once"):
            response = self.client.list_options(self.project_id)
        assert len(response) > 0
        assert all(isinstance(option, Option) for option in response)

    def test_schedule_download(self):
        with vcr.use_cassette(str(cassettes_path / "data_export/schedule_download.yaml"), mode="once"):
            option = Option(name="JSONL")
            task_id = self.client.schedule_download(self.project_id, option)
        assert task_id is not None
        assert isinstance(task_id, str)

    def test_download(self):
        with vcr.use_cassette(str(cassettes_path / "data_export/download.yaml"), mode="once"):
            option = Option(name="JSONL")
            task_id = self.client.schedule_download(self.project_id, option)
            time.sleep(1)  # lazy work
            file = self.client.download(self.project_id, task_id)
            assert file.exists()
            assert file.stat().st_size > 0
            file.unlink()
