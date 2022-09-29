from pydantic import BaseModel


class Role(BaseModel):
    """Contains the data relevant to a role on a Doccano project"""

    id: int
    name: str
