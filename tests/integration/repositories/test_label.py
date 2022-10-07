import pytest
import vcr

from doccano_client.models.label import Category
from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.label import CategoryRepository
from tests.conftest import repository_fixtures


@pytest.fixture
def category():
    return Category(example=14073, label=23)


class TestCategoryRepository:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(repository_fixtures / "label/login.yaml"), mode="once"):
            client = BaseRepository("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = CategoryRepository(client)
        cls.project_id = 16

    def test_create(self, category):
        with vcr.use_cassette(str(repository_fixtures / "label/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, category)
        assert response.label == category.label

    def test_update(self, category):
        with vcr.use_cassette(str(repository_fixtures / "label/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, category)
        with vcr.use_cassette(str(repository_fixtures / "label/update.yaml"), mode="once"):
            response.label = 24
            updated = self.client.update(self.project_id, response)
        assert updated.label == response.label
        assert updated.id == response.id

    def test_delete(self, category):
        with vcr.use_cassette(str(repository_fixtures / "label/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, category)
        with vcr.use_cassette(str(repository_fixtures / "label/delete.yaml"), mode="once"):
            self.client.delete(self.project_id, response)
