from __future__ import annotations

from typing import List

from doccano_client.models.user import User
from doccano_client.repositories.base import BaseRepository


class UserRepository:
    """Repository for interacting with the Doccano user API"""

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

    def find_by_name(self, name: str) -> User:
        """Find a user by name

        Args:
            name (str): The name of the user to find

        Returns:
            User: The found user

        Raises:
            ValueError: If the user is not found
        """
        users = self.list(name)
        for user in users:
            if user.username == name:
                return user
        raise ValueError(f"User '{name}' not found")

    def create_user(self, username: str, password: str) -> User:
        """Create new user.

        Args:
            username (str): the username of the user to be created
            password (str): the password to set for the new user

        Returns:
            User: the newly created user info
        """
        response = self._client.post(
            "users/create",
            json={"username": username, "password1": password, "password2": password},
        )
        return User.parse_obj(response.json())
