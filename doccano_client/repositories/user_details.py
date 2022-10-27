from __future__ import annotations

from doccano_client.models.user_details import (
    PasswordChange,
    PasswordUpdated,
    UserDetails,
)
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

    def update_current_user_details(self, user_details: UserDetails) -> UserDetails:
        """Update either username, first name or last name of the current user.
           If any args are left as None the current info will be kept

        Args:
            user_details (UserDetails): The user details.

        Returns:
            UserDetails: the updated user login info
        """
        response = self._client.put("auth/user/", json=user_details.dict())
        return UserDetails.parse_obj(response.json())

    def change_current_user_password(self, password_change: PasswordChange) -> PasswordUpdated:
        """Change the password of the Current User

        Args:
            password_change (PasswordChange): the new password to set for the current user

        Returns:
            PasswordUpdated: Message confirming password change.
        """
        response = self._client.post(
            "auth/password/change/",
            json={"new_password1": password_change.new_password, "new_password2": password_change.confirm_password},
        )
        return PasswordUpdated.parse_obj(response.json())
