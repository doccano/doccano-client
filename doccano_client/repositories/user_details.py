from __future__ import annotations

from doccano_client.models.user_details import UserDetails
from doccano_client.repositories.base import BaseRepository


class UserDetailsRepository:
    """Repository for interacting with the Doccano UserDetails API"""

    def __init__(self, client: BaseRepository):
        self._client = client

    def get_current_user_details(self) -> UserDetails:
        """Get the Current User Details

        Returns:
            UserDetails: The user login info.
        """
        response = self._client.get("auth/user")
        return UserDetails.parse_obj(response.json())
