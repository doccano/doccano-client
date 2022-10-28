from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    is_superuser: bool
    is_staff: bool
