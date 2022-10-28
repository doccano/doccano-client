from typing import Literal, Optional

from pydantic import BaseModel

ROLE_NAME = Literal["project_admin", "annotator", "annotation_approver"]


class Member(BaseModel):
    id: Optional[int]
    user: int
    role: int
    username: str = ""
    rolename: str = ""
