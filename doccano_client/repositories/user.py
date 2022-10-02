from __future__ import annotations

from typing import List

from doccano_client.models.user import User
from doccano_client.repositories.base import BaseRepository


class UserRepository:
    """Repository for interacting with the Doccano user API"""

    resource_type = "label-type"

    def __init__(self, client: BaseRepository):
        self._client = client

    def get_profile(self) -> User:
        """Get a profile

        Returns:
            User: The user.
        """
        response = self._client.get("me")
        return User.parse_obj(response.json())

    def list(self, name: str = "") -> List[User]:
        """Return users

        Args:
            name (str): The name of the user to search for

        Returns:
            User: The list of the users.
        """
        response = self._client.get(f"users?q={name}")
        users = [User.parse_obj(user) for user in response.json()]
        return users
