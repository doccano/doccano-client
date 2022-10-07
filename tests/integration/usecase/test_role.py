import vcr

from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.role import RoleRepository
from doccano_client.usecase.role import RoleUseCase
from tests.conftest import usecase_fixtures


class TestRoleUseCase:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(usecase_fixtures / "login.yaml"), mode="once"):
            base = BaseRepository("http://localhost:8000")
            base.login(username="admin", password="password")
            cls.usecase = RoleUseCase(RoleRepository(base))

    def test_list_roles(self):
        with vcr.use_cassette(str(usecase_fixtures / "role/list.yaml"), mode="once"):
            roles = self.usecase.list()
            assert len(roles) == 3
