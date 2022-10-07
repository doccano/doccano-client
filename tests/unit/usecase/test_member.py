from unittest.mock import MagicMock

import pytest

from doccano_client.models.member import Member
from doccano_client.models.role import Role
from doccano_client.models.user import User
from doccano_client.usecase.member import MemberUseCase


@pytest.fixture
def payload():
    return {"username": "admin", "role_name": "admin"}


class TestMemberUseCase:
    @classmethod
    def setup_method(cls):
        cls.member_repository = MagicMock()
        cls.user_repository = MagicMock()
        cls.role_repository = MagicMock()
        cls.usecase = MemberUseCase(cls.member_repository, cls.user_repository, cls.role_repository)

    def test_find_by_id(self):
        self.usecase.find_by_id(0, 1)
        self.member_repository.find_by_id.assert_called_once_with(0, 1)

    def test_list(self):
        self.usecase.list(0)
        self.member_repository.list.assert_called_once_with(0)

    def test_create(self, payload):
        project_id = 0
        role = Role(id=2, name="annotator")
        user = User(id=1, username="admin", is_superuser=False, is_staff=False)
        member = Member(id=None, user=user.id, role=role.id)
        self.user_repository.find_by_username.return_value = user
        self.role_repository.find_by_name.return_value = role
        self.member_repository.create.return_value = member
        self.usecase.add(project_id, **payload)
        self.member_repository.create.assert_called_once_with(project_id, member)

    def test_update(self):
        project_id = 0
        member = Member(id=0, user=0, role=0)
        role = Role(id=2, name="annotator")
        self.member_repository.find_by_id.return_value = member
        self.role_repository.find_by_name.return_value = role
        self.usecase.update(project_id, member.id, role_name=role.name)
        member.role = role.id
        self.member_repository.update.assert_called_once_with(project_id, member)

    def test_delete(self):
        self.usecase.delete(0, 1)
        self.member_repository.delete.assert_called_once_with(0, 1)
