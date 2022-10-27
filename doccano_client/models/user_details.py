from pydantic import BaseModel, root_validator
from pydantic.types import ConstrainedStr


class UserDetails(BaseModel):
    """Contains the data relevant to a user on a Doccano project"""

    pk: int
    username: str
    email: str
    first_name: str
    last_name: str


class PasswordUpdated(BaseModel):
    """Contains the data relevant to a password adjustment"""

    detail: str


class Password(ConstrainedStr):
    min_length = 2
    max_length = 128
    strip_whitespace = True


class PasswordChange(BaseModel):
    new_password: Password
    confirm_password: Password

    @root_validator
    def new_password_matches_confirm_password(cls, values):
        new_password = values.get("new_password")
        confirm_password = values.get("confirm_password")
        if new_password != confirm_password:
            raise ValueError("The new password does not match the confirm one.")
        return values
