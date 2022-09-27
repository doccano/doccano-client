from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class Span(DataClassJsonMixin):
    """Represents an annotation on an example in a Sequence Labeling project."""

    label: int
    prob: float
    start_offset: int
    end_offset: int
