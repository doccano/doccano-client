from doccano_client.models.user_details import (
    PasswordChange,
    PasswordUpdated,
    UserDetails,
)
from doccano_client.repositories.user_details import UserDetailsRepository


class UserDetailsUseCase:
    def __init__(self, user_details_repository: UserDetailsRepository):
        self._user_details_repository = user_details_repository

    def get_current_user_details(self) -> UserDetails:
        """Get the Current User Details

        Returns:
            UserDetails: The user login info.
        """
        return self._user_details_repository.get_current_user_details()

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
        user_details = self.get_current_user_details()
        user_details = UserDetails(
            pk=user_details.pk,
            username=username or user_details.username,
            first_name=first_name or user_details.first_name,
            last_name=last_name or user_details.last_name,
            email=user_details.email,
        )
        return self._user_details_repository.update_current_user_details(user_details)

    def change_current_user_password(self, password: str, confirm_password: str) -> PasswordUpdated:
        """Change the password of the current user

        Args:
            password (str): the new password to set for the current user
            confirm_password (str): confirm the new password to set for the current user

        Returns:
            PasswordUpdated: Message confirming password change.
        """
        password_change = PasswordChange(new_password=password, confirm_password=confirm_password)
        return self._user_details_repository.change_current_user_password(password_change)
