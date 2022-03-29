from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from dataclasses_json import DataClassJsonMixin

from . import Annotation


@dataclass
class Example(DataClassJsonMixin):
    """Contains the data and operations relevant to a example on a Doccano project"""

    text: str
    meta: Dict[str, Any] = field(default_factory=dict)
    annotation_approver: Optional[str] = None
    annotations: List[Annotation] = field(default_factory=list)
    comment_count: int = 0


# TODO: Retained for backwards compatibility. Remove in v1.6.0
Document = Example
