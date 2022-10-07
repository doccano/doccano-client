import pytest
import vcr

from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.comment import CommentRepository
from doccano_client.repositories.example import ExampleRepository
from doccano_client.repositories.project import ProjectRepository
from doccano_client.usecase.comment import CommentUseCase
from doccano_client.usecase.example import ExampleUseCase
from doccano_client.usecase.project import ProjectUseCase
from tests.conftest import usecase_fixtures


class TestCommentUseCase:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(usecase_fixtures / "login.yaml"), mode="once"):
            base = BaseRepository("http://localhost:8000")
            base.login(username="admin", password="password")
            cls.project = ProjectUseCase(ProjectRepository(base))
            cls.example = ExampleUseCase(ExampleRepository(base))
            cls.comment = CommentUseCase(CommentRepository(base))

    def test_create_comment(self):
        with vcr.use_cassette(str(usecase_fixtures / "comment/create.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            example = self.example.create(project.id, text="test")
            comment = self.comment.create(project.id, example.id, text="test")
            assert comment.text == "test"

    def test_update_comment(self):
        with vcr.use_cassette(str(usecase_fixtures / "comment/update.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            example = self.example.create(project.id, text="test")
            comment = self.comment.create(project.id, example.id, text="test")
            comment.text = "test2"
            updated_comment = self.comment.update(project.id, comment.id, text=comment.text)
            assert comment == updated_comment

    def test_delete_comment(self):
        with vcr.use_cassette(str(usecase_fixtures / "comment/delete.yaml"), mode="once"):
            project = self.project.create(name="test", project_type="DocumentClassification", description="test")
            example = self.example.create(project.id, text="test")
            comment = self.comment.create(project.id, example.id, text="test")
            self.comment.delete(project.id, comment.id)
            with pytest.raises(Exception):
                self.comment.find_by_id(project.id, comment.id)
