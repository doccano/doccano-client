from typing import List

from pydantic import BaseModel


class LabelCount(BaseModel):
    label: str
    count: int


class LabelDistribution(BaseModel):
    username: str
    counts: List[LabelCount]


class Progress(BaseModel):
    total: int
    remaining: int
    completed: int

    def is_finished(self) -> bool:
        return self.remaining == 0


class MemberProgress(BaseModel):
    username: str
    progress: Progress
