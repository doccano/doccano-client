from typing import Any, Optional

from pydantic import BaseModel


class TaskStatus(BaseModel):
    ready: bool = False
    result: Optional[Any] = None
    error: Optional[Any] = None
