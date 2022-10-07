from typing import Any, Optional

from pydantic import BaseModel


class TaskStatus(BaseModel):
    """Contains the data relevant to a task status on a Doccano project"""

    ready: bool = False
    result: Optional[Any] = None
    error: Optional[Any] = None
