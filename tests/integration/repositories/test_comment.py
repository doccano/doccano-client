import pytest
import vcr

from doccano_client.models.comment import Comment
from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.comment import CommentRepository
from tests.conftest import repository_fixtures


@pytest.fixture
def comment():
    return Comment(text="Test comment", example=14069)


class TestCommentRepository:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(repository_fixtures / "comment/login.yaml"), mode="once"):
            client = BaseRepository("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = CommentRepository(client)
        cls.project_id = 16

    def test_create(self, comment):
        with vcr.use_cassette(str(repository_fixtures / "comment/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, comment)
        assert response.text == comment.text

    def test_update(self, comment):
        with vcr.use_cassette(str(repository_fixtures / "comment/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, comment)
        with vcr.use_cassette(str(repository_fixtures / "comment/update.yaml"), mode="once"):
            response.text = "Updated Type"
            updated = self.client.update(self.project_id, response)
        assert updated.text == "Updated Type"
        assert updated.id == response.id

    def test_delete(self, comment):
        with vcr.use_cassette(str(repository_fixtures / "comment/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, comment)
        with vcr.use_cassette(str(repository_fixtures / "comment/delete.yaml"), mode="once"):
            self.client.delete(self.project_id, response.id)
