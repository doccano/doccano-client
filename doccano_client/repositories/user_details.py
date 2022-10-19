from __future__ import annotations

from doccano_client.models.user_details import UserDetails
from doccano_client.repositories.base import BaseRepository


class PasswordLengthError(Exception):
    """Exception raised for errors where the password doesn't have the correct length.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str = "Password can't be greater than 128 characters or less than 2 character"):
        self.message = message
        super().__init__(self.message)


class PasswordMismatchError(Exception):
    """Exception raised for errors where the password and confirm password doesn't match.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str = "Please make sure the password and confirm_password parameters match"):
        self.message = message
        super().__init__(self.message)


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

        Args:
            password (str): the new password to set for the current user
            confirm_password(str): confirm the new password to set for the current user

        Returns:
            Not Sure Yet

        Raises:
            PasswordLengthError: If the password is longer than 128 chars or shorter than 2 chars
            PasswordMismatchError: If the password and confirm_password do not match
        """
        if len(password) > 128 or len(password) < 2:
            raise PasswordLengthError()
        if password != confirm_password:
            raise PasswordMismatchError()
        response = self._client.post("auth/password/change/", new_password1 = password, new_password2 = confirm_password)
        return response
