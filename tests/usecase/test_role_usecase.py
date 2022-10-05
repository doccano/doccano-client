from unittest.mock import MagicMock

from doccano_client.usecase.role import RoleUseCase


class TestRoleUseCase:
    @classmethod
    def setup_class(cls):
        cls.role_repository = MagicMock()
        cls.role_usecase = RoleUseCase(cls.role_repository)

    def test_list(self):
        self.role_usecase.list()
        self.role_repository.list.assert_called_once()
