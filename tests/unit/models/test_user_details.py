import pytest

from doccano_client.models.user_details import PasswordChange


class TestPasswordChange:
    def test_correct_password(self):
        password_change = PasswordChange(new_password="foobarbaz", confirm_password="foobarbaz")
        assert password_change.new_password == password_change.confirm_password

    def test_raise_error_with_short_password(self):
        with pytest.raises(ValueError):
            PasswordChange(new_password="f", confirm_password="f")

    def test_raise_error_with_long_password(self):
        with pytest.raises(ValueError):
            PasswordChange(new_password="f" * 129, confirm_password="f" * 129)

    def test_raise_error_if_new_password_does_not_match_confirm_password(self):
        with pytest.raises(ValueError):
            PasswordChange(new_password="foobarbaz", confirm_password="zabraboof")
