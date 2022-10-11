from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Example(BaseModel):
    """Contains the data relevant to a example on a Doccano project"""

    id: Optional[int]
    text: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)
    annotation_approver: Optional[str] = None
    comment_count: int = 0
    is_confirmed: bool = False
    filename: str = ""
    upload_name: str = ""
