import pathlib

import vcr

from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.data_download import DataDownloadRepository
from doccano_client.repositories.data_upload import DataUploadRepository
from doccano_client.repositories.project import ProjectRepository
from doccano_client.repositories.task_status import TaskStatusRepository
from doccano_client.usecase.data_download import DataDownloadUseCase
from doccano_client.usecase.data_upload import DataUploadUseCase
from doccano_client.usecase.project import ProjectUseCase
from tests.conftest import usecase_fixtures

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"


class TestDataDownloadUseCase:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(usecase_fixtures / "login.yaml"), mode="once"):
            base = BaseRepository("http://localhost:8000")
            base.login(username="admin", password="password")
            cls.project = ProjectUseCase(ProjectRepository(base))
            cls.data_download = DataDownloadUseCase(
                DataDownloadRepository(base),
                TaskStatusRepository(base),
            )
            cls.data_import = DataUploadUseCase(
                DataUploadRepository(base),
                TaskStatusRepository(base),
            )

    def test_data_download(self):
        with vcr.use_cassette(str(usecase_fixtures / "data_download/download.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            file_path = DATA_DIR / "classification.jsonl"
            self.data_import.upload(
                project.id,
                file_paths=[file_path],
                task="DocumentClassification",
                format="JSONL",
                column_data="text",
                column_label="labels",
            )
            path = self.data_download.download(project.id, format="JSONL")
            assert path.exists()
            assert path.stat().st_size > 0
            path.unlink()
