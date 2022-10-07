from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class Text(DataClassJsonMixin):
    """Represents an annotation on an example in a Seq2seq project."""

    text: str
    prob: float
