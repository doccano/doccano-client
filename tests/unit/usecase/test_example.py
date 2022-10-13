from unittest.mock import MagicMock

import pytest

from doccano_client.models.example import Example
from doccano_client.usecase.example import ExampleUseCase


@pytest.fixture
def payload():
    return {
        "text": "Test",
    }


class TestExampleUseCase:
    @classmethod
    def setup_method(cls):
        cls.repository = MagicMock()
        cls.usecase = ExampleUseCase(cls.repository)

    def test_find_by_id(self):
        self.usecase.find_by_id(0, 1)
        self.repository.find_by_id.assert_called_once_with(0, 1)

    def test_list(self):
        list(self.usecase.list(0))
        self.repository.list.assert_called_once_with(0, None)

    def test_create(self, payload):
        project_id = 0
        self.usecase.create(project_id, **payload)
        self.repository.create.assert_called_once_with(project_id, Example.parse_obj(payload))

    def test_update(self, payload):
        project_id = 0
        example = Example(id=1, text="Test text")
        self.repository.find_by_id.return_value = example
        self.usecase.update(project_id, example.id, **payload)
        example.text = payload["text"]
        self.repository.find_by_id.assert_called_once_with(project_id, example.id)
        self.repository.update.assert_called_once_with(project_id, example)

    def test_delete(self):
        self.usecase.delete(0, 1)
        self.repository.delete.assert_called_once_with(0, 1)
