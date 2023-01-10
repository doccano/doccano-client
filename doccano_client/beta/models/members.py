from dataclasses import dataclass


@dataclass
class Member:
    """Contains the data and operations relevant to a Member on a Doccano project"""

    user: int
    role: int
