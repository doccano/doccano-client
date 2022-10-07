import pathlib

import vcr

from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.data_upload import DataUploadRepository
from doccano_client.repositories.example import ExampleRepository
from doccano_client.repositories.project import ProjectRepository
from doccano_client.repositories.task_status import TaskStatusRepository
from doccano_client.usecase.data_upload import DataUploadUseCase
from doccano_client.usecase.example import ExampleUseCase
from doccano_client.usecase.project import ProjectUseCase
from tests.conftest import usecase_fixtures

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"


class TestDataUploadUseCase:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(usecase_fixtures / "login.yaml"), mode="once"):
            base = BaseRepository("http://localhost:8000")
            base.login(username="admin", password="password")
            cls.project = ProjectUseCase(ProjectRepository(base))
            cls.example = ExampleUseCase(ExampleRepository(base))
            cls.data_upload = DataUploadUseCase(
                DataUploadRepository(base),
                TaskStatusRepository(base),
            )

    def test_data_upload(self):
        with vcr.use_cassette(str(usecase_fixtures / "data_upload/upload.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            file_path = DATA_DIR / "classification.jsonl"
            self.data_upload.upload(
                project.id,
                file_paths=[file_path],
                task="DocumentClassification",
                format="JSONL",
                column_data="text",
                column_label="labels",
            )
            examples = self.example.list(project.id)
            assert len(list(examples)) == 3
