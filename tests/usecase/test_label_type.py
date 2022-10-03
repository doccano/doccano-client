from unittest.mock import MagicMock

import pytest

from doccano_client.models.label_type import LabelType
from doccano_client.usecase.label_type import LabelTypeUseCase


@pytest.fixture
def payload():
    return {
        "text": "Test Label Type",
        "color": "#000000",
    }


class TestLabelTypeUseCase:
    @classmethod
    def setup_class(cls):
        cls.label_type_repository = MagicMock()
        cls.label_type_usecase = LabelTypeUseCase(cls.label_type_repository)

    def test_find_by_id(self):
        self.label_type_usecase.find_by_id(0, 1)
        self.label_type_repository.find_by_id.assert_called_once_with(0, 1)

    def test_list(self):
        self.label_type_usecase.list(0)
        self.label_type_repository.list.assert_called_once_with(0)

    def test_create(self, payload):
        project_id = 0
        self.label_type_usecase.create(project_id, **payload)
        payload["background_color"] = payload.pop("color")
        self.label_type_repository.create.assert_called_once_with(project_id, LabelType.parse_obj(payload))

    def test_update(self, payload):
        project_id = 0
        label_type_id = 1
        self.label_type_usecase.update(project_id, label_type_id, **payload)
        payload["id"] = label_type_id
        payload["background_color"] = payload.pop("color")
        self.label_type_repository.update.assert_called_once_with(project_id, LabelType.parse_obj(payload))

    def test_delete(self):
        self.label_type_usecase.delete(0, 1)
        self.label_type_repository.delete.assert_called_once_with(0, 1)
