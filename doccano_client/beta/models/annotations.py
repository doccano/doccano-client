from dataclasses import dataclass
from typing import Union

from dataclasses_json import DataClassJsonMixin


@dataclass
class CategoryAnnotation(DataClassJsonMixin):
    """Represents an annotation on an example in a Text Classification project."""

    label: int
    prob: float


@dataclass
class SpanAnnotation(DataClassJsonMixin):
    """Represents an annotation on an example in a Sequence Labeling project."""

    label: int
    prob: float
    start_offset: int
    end_offset: int


@dataclass
class TextLabelAnnotation(DataClassJsonMixin):
    """Represents an annotation on an example in a Seq2seq project."""

    text: str
    prob: float


Annotation = Union[CategoryAnnotation, SpanAnnotation, TextLabelAnnotation]
