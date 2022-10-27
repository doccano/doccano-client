import vcr

from doccano_client.models.user_details import PasswordUpdated
from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.user_details import UserDetailsRepository
from doccano_client.usecase.user_details import UserDetailsUseCase
from tests.conftest import usecase_fixtures


class TestUserDetailsUseCase:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(usecase_fixtures / "user_details/login.yaml"), mode="once"):
            base = BaseRepository("http://localhost:8000")
            base.login(username="admin", password="foobarbaz")
            cls.usecase = UserDetailsUseCase(UserDetailsRepository(base))

    def test_get_current_user_details(self):
        with vcr.use_cassette(str(usecase_fixtures / "user_details/get.yaml"), mode="once"):
            user_details = self.usecase.get_current_user_details()
            assert user_details.username == "admin"

    def test_update_user_details(self):
        with vcr.use_cassette(str(usecase_fixtures / "user_details/update_user_details.yaml"), mode="once"):
            self.usecase.update_current_user_details(username="admin1")
            user_details = self.usecase.get_current_user_details()
            assert user_details.username == "admin1"
            self.usecase.update_current_user_details(username="admin")

    def test_change_password(self):
        with vcr.use_cassette(str(usecase_fixtures / "user_details/change_password.yaml"), mode="once"):
            updated = self.usecase.change_current_user_password(password="foobarbaz1", confirm_password="foobarbaz1")
            assert isinstance(updated, PasswordUpdated)
            self.usecase.change_current_user_password(password="foobarbaz", confirm_password="foobarbaz")
