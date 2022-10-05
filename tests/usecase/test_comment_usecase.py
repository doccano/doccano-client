from unittest.mock import MagicMock

import pytest

from doccano_client.models.comment import Comment
from doccano_client.usecase.comment import CommentUseCase


@pytest.fixture
def payload():
    return {
        "text": "Test",
    }


class TestCommentUseCase:
    @classmethod
    def setup_method(cls):
        cls.repository = MagicMock()
        cls.usecase = CommentUseCase(cls.repository)

    def test_find_by_id(self):
        self.usecase.find_by_id(0, 1)
        self.repository.find_by_id.assert_called_once_with(0, 1)

    def test_list(self):
        list(self.usecase.list(0, 1, ""))
        self.repository.list.assert_called_once_with(0, 1, "")

    def test_create(self, payload):
        project_id = 0
        example_id = 1
        self.usecase.create(project_id, example_id, **payload)
        payload["example"] = example_id
        self.repository.create.assert_called_once_with(project_id, Comment.parse_obj(payload))

    def test_update(self, payload):
        project_id = 0
        example_id = 1
        comment_id = 2
        self.usecase.update(project_id, example_id, comment_id, **payload)
        payload["id"] = comment_id
        payload["example"] = example_id
        self.repository.update.assert_called_once_with(project_id, Comment.parse_obj(payload))

    def test_delete(self):
        self.usecase.delete(0, 1)
        self.repository.delete.assert_called_once_with(0, 1)
