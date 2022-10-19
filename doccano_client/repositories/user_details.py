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
        response = self._client.get("auth/user/")
        return UserDetails.parse_obj(response.json())

    def change_current_user_password(self, password: str, confirm_password: str):
        """Change the password of the Current User

        Returns:
            Not Sure Yet
        """
        if len(password) > 128:
            raise Exception("Password can't be greater than 128 characters")
        if password != confirm_password:
            raise Exception("Please make sure the password and confirm_password parameters match")
        response = self._client.post("auth/password/change/", "new_password1" = password, "new_password2" = confirm_password})
        return response