from pydantic import BaseModel


class Option(BaseModel):
    name: str
    example: str = ""
