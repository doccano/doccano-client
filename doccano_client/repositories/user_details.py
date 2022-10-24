from __future__ import annotations

from doccano_client.models.user_details import PasswordChange, UserDetails
from doccano_client.repositories.base import BaseRepository


class PasswordLengthError(Exception):
    """Exception raised for errors where the password doesn't have the correct length.

    Attributes:
        message -- explanation of the error
    """

    def __init__(
        self,
        message: str = "Password can't be greater than 128 characters or less than 2 character",
    ):
        self.message = message
        super().__init__(self.message)


class PasswordMismatchError(Exception):
    """Exception raised for errors where the password and confirm password doesn't match.

    Attributes:
        message -- explanation of the error
    """

    def __init__(
        self,
        message: str = "Please make sure the password and confirm_password parameters match",
    ):
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

    def update_current_user_details(
        self, username: str = None, first_name: str = None, last_name: str = None
    ) -> UserDetails:
        """Update either username, first name or last name of the current user.
           If any args are left as None the current info will be kept

        Args:
            username (str): The username to change the current user to.
            first_name (str): The first name to change the current user to.
            last_name (str): The last name to change the current user to

        Returns:
            UserDetails: the updated user login info
        """
        if any(par is None for par in [username, first_name, last_name]):
            current_user_details = self.get_current_user_details()
            if username is None:
                username = current_user_details.username
            if first_name is None:
                first_name = current_user_details.first_name
            if last_name is None:
                last_name = current_user_details.last_name
        response = self._client.post(
            "auth/user/", json={"username": username, "first_name": first_name, "last_name": last_name}
        )
        return UserDetails.parse_obj(response.json())

    def change_current_user_password(self, password: str, confirm_password: str) -> PasswordChange:
        """Change the password of the Current User

        Args:
            password (str): the new password to set for the current user
            confirm_password(str): confirm the new password to set for the current user

        Returns:
            PasswordChange: Message confirming password change.

        Raises:
            PasswordLengthError: If the password is longer than 128 chars or shorter than 2 chars
            PasswordMismatchError: If the password and confirm_password do not match
        """
        if len(password) > 128 or len(password) < 2:
            raise PasswordLengthError()
        if password != confirm_password:
            raise PasswordMismatchError()
        response = self._client.post(
            "auth/password/change/",
            json={"new_password1": password, "new_password2": confirm_password},
        )
        return PasswordChange.parse_obj(response.json())

    def create_new_user(self, username: str, password: str, confirm_password: str):
        """Create new user

        Args:
            username (str): the username of the user thats to be created
            password (str): the password to set for the new user
            confirm_password(str): confirm the password to set for the new user
        
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
        response = self._client.post(
            "auth/user/add/",
            json={"username": username,"password1": password, "password2": confirm_password, "_save": "Save"}
        )
        return response.json()
        