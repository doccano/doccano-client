from typing import List

from doccano_client.models.member import Member
from doccano_client.repositories.member import MemberRepository
from doccano_client.repositories.role import RoleRepository
from doccano_client.repositories.user import UserRepository


class MemberUseCase:
    def __init__(
        self, member_repository: MemberRepository, user_repository: UserRepository, role_repository: RoleRepository
    ):
        self._member_repository = member_repository
        self._user_repository = user_repository
        self._role_repository = role_repository

    def find_by_id(self, project_id: int, member_id: int) -> Member:
        """Find a member by id

        Args:
            project_id (int): The id of the project to find
            member_id (int): The id of the member to find

        Returns:
            Member: The found member
        """
        return self._member_repository.find_by_id(project_id, member_id)

    def list(self, project_id: int) -> List[Member]:
        """Return all members

        Args:
            project_id (int): The id of the project

        Returns:
            List[Member]: The members in the project.
        """
        return self._member_repository.list(project_id)

    def add(
        self,
        project_id: int,
        username: str,
        role_name: str,
    ) -> Member:
        """Create a new member

        Args:
            project_id (int): The id of the project
            username (str): The username of the future member
            role_name (str): The role of the future member

        Returns:
            Member: The created member
        """
        user = self._user_repository.find_by_name(username)
        role = self._role_repository.find_by_name(role_name)
        member = Member(user=user.id, role=role.id)
        return self._member_repository.create(project_id, member)

    def update(
        self,
        project_id: int,
        member_id: int,
        role_name: str,
    ) -> Member:
        """Update a member role

        Args:
            project_id (int): The id of the project
            member_id (int): The id of the member
            role_name (str): The role of the member

        Returns:
            Member: The updated member
        """
        member = self.find_by_id(project_id, member_id)
        role = self._role_repository.find_by_name(role_name)
        member.role = role.id
        return self._member_repository.update(project_id, member)

    def delete(self, project_id: int, member_id: int):
        """Delete a member.

        Args:
            project_id (int): The project id.
            member_id (int): The member id.
        """
        self._member_repository.delete(project_id, member_id)

    def bulk_delete(self, project_id: int, member_ids: List[int]):
        """Bulk delete members

        Args:
            project_id (int): The id of the project
            member_ids (List[int]): The list of member ids to delete
        """
        self._member_repository.bulk_delete(project_id, member_ids)
