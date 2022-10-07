from unittest.mock import MagicMock

from doccano_client.models.label_type import LabelType
from doccano_client.services.label_type import LabelTypeService


class TestLabelTypeService:
    @classmethod
    def setup_method(cls):
        cls.repository = MagicMock()
        cls.service = LabelTypeService(cls.repository)

    def test_return_false_if_label_type_does_not_exist(self):
        label_type = LabelType(id=1, text="Test")
        self.repository.list.return_value = []
        assert not self.service.exists(0, label_type)

    def test_return_true_if_same_text_exists(self):
        label_type = LabelType(id=1, text="Test")
        self.repository.list.return_value = [LabelType(id=2, text="Test")]
        assert self.service.exists(0, label_type)

    def test_return_true_if_same_key_exists(self):
        label_type = LabelType(id=1, text="Test", suffix_key="t")
        self.repository.list.return_value = [LabelType(id=2, text="Test2", suffix_key="t")]
        assert self.service.exists(0, label_type)

    def test_return_false_if_same_key_exists_but_id_is_same(self):
        label_type = LabelType(id=1, text="Test", suffix_key="t")
        self.repository.list.return_value = [LabelType(id=1, text="Test2", suffix_key="t")]
        assert not self.service.exists(0, label_type)

    def test_return_false_if_same_text_exists_but_id_is_same(self):
        label_type = LabelType(id=1, text="Test")
        self.repository.list.return_value = [label_type]
        assert not self.service.exists(0, label_type)
