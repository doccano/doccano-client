import vcr

from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.role import RoleRepository
from tests.conftest import cassettes_path


class TestRoleRepository:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(cassettes_path / "role/login.yaml"), mode="once"):
            client = BaseRepository("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = RoleRepository(client)

    def test_list(self):
        with vcr.use_cassette(str(cassettes_path / "role/list.yaml"), mode="once"):
            roles = self.client.list()
            assert len(roles) == 3
