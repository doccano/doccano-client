from unittest.mock import MagicMock

from doccano_client.models.label import Label
from doccano_client.usecase.label import LabelUseCase


class TestLabelUseCase:
    @classmethod
    def setup_method(cls):
        cls.label_repository = MagicMock()
        cls.label_type_repository = MagicMock()
        cls.usecase = LabelUseCase(cls.label_repository, cls.label_type_repository)

    def test_find_by_id(self):
        self.usecase.find_by_id(0, 1, 2)
        self.label_repository.find_by_id.assert_called_once_with(0, 1, 2)

    def test_list(self):
        self.usecase.list(0, 1)
        self.label_repository.list.assert_called_once_with(0, 1)

    def test_delete(self):
        label = Label(id=2, example=1)
        self.label_repository.find_by_id.return_value = label
        self.usecase.delete(0, 1, 2)
        self.label_repository.find_by_id.assert_called_once_with(0, 1, 2)
        self.label_repository.delete.assert_called_once_with(0, label)

    def test_delete_all(self):
        self.usecase.delete_all(0, 1)
        self.label_repository.delete_all.assert_called_once_with(0, 1)
