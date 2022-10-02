import pytest
import vcr

from doccano_client.models.example import Example
from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.example import ExampleRepository
from tests.conftest import cassettes_path


@pytest.fixture
def example():
    return Example(text="Test Example")


class TestExampleRepository:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(cassettes_path / "example/login.yaml"), mode="once"):
            client = BaseRepository("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = ExampleRepository(client)
        cls.project_id = 16

    def test_create(self, example):
        with vcr.use_cassette(str(cassettes_path / "example/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, example)
        assert response.text == example.text

    def test_update(self, example):
        with vcr.use_cassette(str(cassettes_path / "example/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, example)
        with vcr.use_cassette(str(cassettes_path / "example/update.yaml"), mode="once"):
            response.text = "Updated Example"
            updated = self.client.update(self.project_id, response)
        assert updated.text == "Updated Example"
        assert updated.id == response.id

    def test_delete(self, example):
        with vcr.use_cassette(str(cassettes_path / "example/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, example)
        with vcr.use_cassette(str(cassettes_path / "example/delete.yaml"), mode="once"):
            self.client.delete(self.project_id, response.id)
