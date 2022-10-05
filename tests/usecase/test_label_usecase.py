from unittest.mock import MagicMock

from doccano_client.models.label import Category, Label
from doccano_client.usecase.label import CategoryUseCase, LabelUseCase


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


class TestCategoryUseCase:
    @classmethod
    def setup_method(cls):
        cls.label_repository = MagicMock()
        cls.label_type_repository = MagicMock()
        cls.usecase = CategoryUseCase(cls.label_repository, cls.label_type_repository)
        cls.name = "Test"
        cls.project_id = 0
        cls.example_id = 1
        cls.label_type_id = 2
        cls.label_id = 3
        cls.category = Category(label=cls.label_type_id, example=cls.example_id)
        cls.label_type_repository.find_by_name.return_value = MagicMock(id=cls.label_type_id)

    def test_create(self):
        self.usecase.create(self.project_id, self.example_id, self.name)
        self.label_type_repository.find_by_name.assert_called_once_with(self.project_id, self.name)
        self.label_repository.create.assert_called_once_with(self.project_id, self.category)

    def test_update(self):
        self.label_repository.find_by_id.return_value = self.category

        self.usecase.update(self.project_id, self.example_id, self.label_id, self.name)
        self.label_type_repository.find_by_name.assert_called_once_with(self.project_id, self.name)
        self.label_repository.update.assert_called_once_with(self.project_id, self.category)
