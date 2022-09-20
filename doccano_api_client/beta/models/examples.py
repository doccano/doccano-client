from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from dataclasses_json import DataClassJsonMixin


@dataclass
class Example(DataClassJsonMixin):
    """Contains the data and operations relevant to a example on a Doccano project"""

    text: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)
    annotation_approver: Optional[str] = None
    comment_count: int = 0
    is_confirmed: bool = False


# TODO: Retained for backwards compatibility. Remove in v1.6.0
Document = Example
