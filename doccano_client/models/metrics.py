from typing import List

from pydantic import BaseModel


class LabelCount(BaseModel):
    """Contains the data relevant to a label frequency on a Doccano project"""

    label: str
    count: int


class LabelDistribution(BaseModel):
    """Contains the data relevant to a role on a Doccano project"""

    username: str
    counts: List[LabelCount]


class Progress(BaseModel):
    total: int
    remaining: int
    completed: int


class MemberProgress(BaseModel):
    username: str
    progress: Progress
