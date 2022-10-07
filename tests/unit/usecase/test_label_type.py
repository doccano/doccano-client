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
    def setup_method(cls):
        cls.label_type_repository = MagicMock()
        cls.label_type_service = MagicMock()
        cls.label_type_service.exists.return_value = False
        cls.label_type_usecase = LabelTypeUseCase(cls.label_type_repository, cls.label_type_service)

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

    def test_cannot_create_duplicate_label_type(self, payload):
        project_id = 0
        self.label_type_service.exists.return_value = True
        with pytest.raises(ValueError):
            self.label_type_usecase.create(project_id, **payload)

    def test_update(self):
        project_id = 0
        label_type = LabelType(id=1, text="Test Label Type", background_color="#000000")
        self.label_type_repository.find_by_id.return_value = label_type
        self.label_type_usecase.update(project_id, label_type.id, text="New Label Type")
        label_type.text = "New Label Type"
        self.label_type_repository.update.assert_called_once_with(project_id, label_type)

    def test_cannot_update_duplicate_label_type(self, payload):
        project_id = 0
        label_type_id = 1
        self.label_type_service.exists.return_value = True
        with pytest.raises(ValueError):
            self.label_type_usecase.update(project_id, label_type_id, **payload)

    def test_delete(self):
        self.label_type_usecase.delete(0, 1)
        self.label_type_repository.delete.assert_called_once_with(0, 1)
