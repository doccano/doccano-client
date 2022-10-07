from pydantic import BaseModel


class User(BaseModel):
    """Contains the data relevant to a user on a Doccano project"""

    id: int
    username: str
    is_superuser: bool
    is_staff: bool
