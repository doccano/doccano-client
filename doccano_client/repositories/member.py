from __future__ import annotations

from typing import List

from doccano_client.models.member import Member
from doccano_client.repositories.base import BaseRepository


class MemberRepository:
    """Repository for interacting with the Doccano member API"""

    def __init__(self, client: BaseRepository):
        self._client = client

    def find_by_id(self, project_id: int, member_id: int) -> Member:
        """Find a member by id

        Args:
            project_id (int): The id of the project
            member_id (int): The id of the member to find

        Returns:
            Member: The found member
        """
        resource = f"projects/{project_id}/members/{member_id}"
        response = self._client.get(resource)
        return Member.parse_obj(response.json())

    def list(self, project_id: int) -> List[Member]:
        """Return all member in which you are a member

        Args:
            project_id (int): The id of the project

        Returns:
            Member: The list of the member.
        """
        resource = f"projects/{project_id}/members"
        response = self._client.get(resource)
        members = [Member.parse_obj(member) for member in response.json()]
        return members

    def create(self, project_id: int, member: Member) -> Member:
        """Create a new member

        Args:
            project_id (int): The id of the project
            member (Member): The member to create

        Returns:
            Member: The created member
        """
        resource = f"projects/{project_id}/members"
        response = self._client.post(resource, json=member.dict(exclude={"id", "username", "rolename"}))
        return Member.parse_obj(response.json())

    def update(self, project_id: int, member: Member) -> Member:
        """Update a member

        Args:
            project_id (int): The id of the project
            member (Member): The member to update

        Returns:
            Member: The updated member

        Raises:
            ValueError: If the member id is not set
        """
        if member.id is None:
            raise ValueError("Member id is required")
        resource = f"projects/{project_id}/members/{member.id}"
        response = self._client.put(resource, json=member.dict(exclude={"username", "rolename"}))
        return Member.parse_obj(response.json())

    def delete(self, project_id: int, member: Member | int):
        """Delete a member

        Args:
            project_id (int): The id of the project
            member (Member | int): The member to delete

        Raises:
            ValueError: If the member id is not set
        """
        if isinstance(member, Member) and member.id is None:
            raise ValueError("Member id is required")
        member_id = member if isinstance(member, int) else member.id
        self.bulk_delete(project_id, [member_id])  # type: ignore

    def bulk_delete(self, project_id: int, members: List[int] | List[Member]):
        """Bulk delete members

        Args:
            project_id (int): The id of the project
            members (List[int] | List[Member]): The list of member ids to delete
        """
        ids = [member if isinstance(member, int) else member.id for member in members]
        self._client.delete(f"projects/{project_id}/members", json={"ids": ids})
