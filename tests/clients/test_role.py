import vcr

from doccano_client.client import DoccanoClient
from doccano_client.clients.role import RoleClient
from tests.conftest import cassettes_path


class TestRoleClient:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(cassettes_path / "role/login.yaml"), mode="once"):
            client = DoccanoClient("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = RoleClient(client)

    def test_list(self):
        with vcr.use_cassette(str(cassettes_path / "role/list.yaml"), mode="once"):
            roles = self.client.list()
            assert len(roles) == 3
