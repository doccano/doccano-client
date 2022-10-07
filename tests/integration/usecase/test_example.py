import pytest
import vcr

from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.example import ExampleRepository
from doccano_client.repositories.project import ProjectRepository
from doccano_client.usecase.example import ExampleUseCase
from doccano_client.usecase.project import ProjectUseCase
from tests.conftest import usecase_fixtures


class TestExampleUseCase:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(usecase_fixtures / "login.yaml"), mode="once"):
            base = BaseRepository("http://localhost:8000")
            base.login(username="admin", password="password")
            cls.project = ProjectUseCase(ProjectRepository(base))
            cls.example = ExampleUseCase(ExampleRepository(base))

    def test_create_example(self):
        with vcr.use_cassette(str(usecase_fixtures / "example/create.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            example = self.example.create(project.id, text="test")
            assert example.text == "test"

    def test_update_example(self):
        with vcr.use_cassette(str(usecase_fixtures / "example/update.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            example = self.example.create(project.id, text="test")
            example.text = "test2"
            updated_example = self.example.update(project.id, example.id, text="test2")
            assert example == updated_example

    def test_delete_example(self):
        with vcr.use_cassette(str(usecase_fixtures / "example/delete.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            example = self.example.create(project.id, text="test")
            self.example.delete(project.id, example.id)
            with pytest.raises(Exception):
                self.example.find_by_id(project.id, example.id)

    def test_delete_all_examples(self):
        with vcr.use_cassette(str(usecase_fixtures / "example/delete_all.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            self.example.create(project.id, text="test")
            self.example.delete_all(project.id)
            examples = self.example.list(project.id)
            assert len(list(examples)) == 0
