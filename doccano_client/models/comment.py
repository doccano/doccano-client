from typing import Optional

from pydantic import BaseModel


class Comment(BaseModel):
    id: Optional[int]
    text: str = ""
    example: int
    user: Optional[int]
    username: Optional[str]
    created_at: Optional[str]
