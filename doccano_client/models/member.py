from typing import Optional

from pydantic import BaseModel


class Member(BaseModel):
    """Contains the data relevant to a member on a Doccano project"""

    id: Optional[int]
    user: int
    role: int
    username: str = ""
    rolename: str = ""
