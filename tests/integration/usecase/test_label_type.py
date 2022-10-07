import pathlib

import pytest
import vcr

from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.label_type import CategoryTypeRepository
from doccano_client.repositories.project import ProjectRepository
from doccano_client.services.label_type import LabelTypeService
from doccano_client.usecase.label_type import LabelTypeUseCase
from doccano_client.usecase.project import ProjectUseCase
from tests.conftest import usecase_fixtures

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"


class TestLabelTypeUseCase:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(usecase_fixtures / "login.yaml"), mode="once"):
            base = BaseRepository("http://localhost:8000")
            base.login(username="admin", password="password")
            cls.project = ProjectUseCase(ProjectRepository(base))
            cls.label_type = LabelTypeUseCase(
                CategoryTypeRepository(base), LabelTypeService(CategoryTypeRepository(base))
            )

    def test_create_label_type(self):
        with vcr.use_cassette(str(usecase_fixtures / "label_type/create.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            label_type = self.label_type.create(project.id, text="text")
            assert label_type.text == "text"

    def test_update_label_type(self):
        with vcr.use_cassette(str(usecase_fixtures / "label_type/update.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            label_type = self.label_type.create(project.id, text="text")
            label_type.text = "text2"
            updated_label_type = self.label_type.update(project.id, label_type_id=label_type.id, text="text2")
            assert label_type == updated_label_type

    def test_delete_label_type(self):
        with vcr.use_cassette(str(usecase_fixtures / "label_type/delete.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            label_type = self.label_type.create(project.id, text="text")
            self.label_type.delete(project.id, label_type.id)
            with pytest.raises(Exception):
                self.label_type.find_by_id(project.id, label_type.id)

    def test_upload_label_type(self):
        with vcr.use_cassette(str(usecase_fixtures / "label_type/upload.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            file_path = DATA_DIR / "labels.json"
            self.label_type.upload(project.id, file_path=file_path)
            label_types = self.label_type.list(project.id)
            assert len(label_types) == 2
