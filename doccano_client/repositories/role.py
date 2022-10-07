from __future__ import annotations

from typing import List

from doccano_client.models.role import Role
from doccano_client.repositories.base import BaseRepository


class RoleRepository:
    """Repository for interacting with the Doccano role API"""

    def __init__(self, client: BaseRepository):
        self._client = client

    def list(self) -> List[Role]:
        """Return all roles

        Returns:
            Role: The list of the roles.
        """
        response = self._client.get("roles")
        roles = [Role.parse_obj(role) for role in response.json()]
        return roles

    def find_by_name(self, name: str) -> Role:
        """Find a role by name

        Args:
            name (str): The name of the role to find

        Returns:
            Role: The found role

        Raises:
            ValueError: If the role is not found
        """
        roles = self.list()
        for role in roles:
            if role.name == name:
                return role
        raise ValueError(f"Role '{name}' not found")
