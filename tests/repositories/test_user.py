import vcr

from doccano_client.models.user import User
from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.user import UserRepository
from tests.conftest import cassettes_path


class TestUserRepository:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(cassettes_path / "user/login.yaml"), mode="once"):
            client = BaseRepository("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = UserRepository(client)

    def test_get_profile(self):
        with vcr.use_cassette(str(cassettes_path / "user/get_profile.yaml"), mode="once"):
            user = self.client.get_profile()
            assert user.username == "admin"

    def test_list(self):
        with vcr.use_cassette(str(cassettes_path / "user/list.yaml"), mode="once"):
            users = self.client.list()
            assert all(isinstance(user, User) for user in users)
