from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class Relation(DataClassJsonMixin):
    """Represents an annotation on an example in a Sequence Labeling project."""

    type: int
    prob: float
    from_id: int
    to_id: int
