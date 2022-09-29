from typing import Optional

from pydantic import BaseModel


class Comment(BaseModel):
    """Contains the data relevant to a comment on a Doccano project"""

    id: Optional[int]
    text: str = ""
    example: int
    user: Optional[int]
    username: Optional[str]
    created_at: Optional[str]
