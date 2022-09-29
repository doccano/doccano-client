from typing import Optional

from pydantic import BaseModel


class TaskStatus(BaseModel):
    """Contains the data relevant to a task status on a Doccano project"""

    ready: bool = False
    result: Optional[dict] = None
    error: Optional[dict] = None
