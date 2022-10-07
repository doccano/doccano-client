import pathlib

import pytest
import vcr

from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.example import ExampleRepository
from doccano_client.repositories.label import CategoryRepository
from doccano_client.repositories.label_type import CategoryTypeRepository
from doccano_client.repositories.project import ProjectRepository
from doccano_client.services.label_type import LabelTypeService
from doccano_client.usecase.example import ExampleUseCase
from doccano_client.usecase.label import CategoryUseCase
from doccano_client.usecase.label_type import LabelTypeUseCase
from doccano_client.usecase.project import ProjectUseCase
from tests.conftest import usecase_fixtures

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"


class TestCategoryUseCase:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(usecase_fixtures / "login.yaml"), mode="once"):
            base = BaseRepository("http://localhost:8000")
            base.login(username="admin", password="password")
            cls.project = ProjectUseCase(ProjectRepository(base))
            cls.example = ExampleUseCase(ExampleRepository(base))
            cls.category_type = LabelTypeUseCase(
                CategoryTypeRepository(base), LabelTypeService(CategoryTypeRepository(base))
            )
            cls.category = CategoryUseCase(CategoryRepository(base), CategoryTypeRepository(base))

    def test_create_label(self):
        with vcr.use_cassette(str(usecase_fixtures / "label/create.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            example = self.example.create(project.id, text="test")
            category_type = self.category_type.create(project.id, text="text")
            category = self.category.create(project.id, example.id, label="text")
            assert category.label == category_type.id

    def test_update_label(self):
        with vcr.use_cassette(str(usecase_fixtures / "label/update.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            example = self.example.create(project.id, text="test")
            self.category_type.create(project.id, text="text")
            category_type = self.category_type.create(project.id, text="text2")
            category = self.category.create(project.id, example.id, label="text")
            category = self.category.update(project.id, example.id, category.id, label="text2")
            assert category.label == category_type.id

    def test_delete_label(self):
        with vcr.use_cassette(str(usecase_fixtures / "label/delete.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            example = self.example.create(project.id, text="test")
            self.category_type.create(project.id, text="text")
            category = self.category.create(project.id, example.id, label="text")
            self.category.delete(project.id, example.id, category.id)
            with pytest.raises(Exception):
                self.category.find_by_id(project.id, example.id, category.id)
