from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class Category(DataClassJsonMixin):
    """Represents an annotation on an example in a Document Classification project."""

    label: int
    prob: float
