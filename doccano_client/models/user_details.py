from pydantic import BaseModel


class UserDetails(BaseModel):
    """Contains the data relevant to a user on a Doccano project"""

    pk: int
    username: str
    email: str
    first_name: str
    last_name: str


class PasswordChange(BaseModel):
    """Contains the data relevant to a password adjustment"""

    detail: str
