from dataclasses import dataclass


@dataclass
class Comment:
    """Contains the data and operations relevant to a comment on a Doccano document"""

    text: str
