import pytest
import vcr

from doccano_client.models.member import Member
from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.member import MemberRepository
from tests.conftest import repository_fixtures


@pytest.fixture
def member():
    return Member(user=3, role=1)


class TestMemberRepository:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(repository_fixtures / "member/login.yaml"), mode="once"):
            client = BaseRepository("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = MemberRepository(client)
        cls.project_id = 16

    def test_create(self, member):
        with vcr.use_cassette(str(repository_fixtures / "member/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, member)
            self.client.delete(self.project_id, response)
        assert response.role == member.role

    def test_update(self, member):
        with vcr.use_cassette(str(repository_fixtures / "member/update.yaml"), mode="once"):
            response = self.client.create(self.project_id, member)
            response.role = 2
            updated = self.client.update(self.project_id, response)
            self.client.delete(self.project_id, response)
        assert updated.role == 2
        assert updated.id == response.id
