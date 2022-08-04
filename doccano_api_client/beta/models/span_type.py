from dataclasses import dataclass
from typing import Optional

LABEL_COLOR_CYCLE = [
    "#EF5350",
    "#7E57C2",
    "#29B6F6",
    "#66BB6A",
    "#FFEE58",
    "#FF7043",
    "#BDBDBD",
    "#EC407A",
    "#5C6BC0",
    "#26C6DA",
    "#9CCC65",
    "#FFCA28",
    "#8D6E63",
    "#AB47BC",
    "#42A5F5",
]


@dataclass
class SpanType:
    """Contains the data and operations relevant to a SpanType on a Doccano project"""

    text: str
    prefix_key: Optional[str] = None
    suffix_key: Optional[str] = None
    background_color: str = LABEL_COLOR_CYCLE[0]
    text_color: str = "#ffffff"
