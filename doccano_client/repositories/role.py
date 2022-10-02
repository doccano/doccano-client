from __future__ import annotations

from typing import List

from doccano_client.client import DoccanoClient
from doccano_client.models.role import Role


class RoleRepository:
    """Repository for interacting with the Doccano role API"""

    resource_type = "label-type"

    def __init__(self, client: DoccanoClient):
        self._client = client

    def list(self) -> List[Role]:
        """Return all roles

        Returns:
            Role: The list of the roles.
        """
        response = self._client.get("roles")
        roles = [Role.parse_obj(role) for role in response.json()]
        return roles
