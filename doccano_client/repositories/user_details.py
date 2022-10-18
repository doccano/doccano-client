from __future__ import annotations

from typing import List

from doccano_client.models.user_details import UserDetails
from doccano_client.repositories.base import BaseRepository


class UserDetailsRepository:
    """Repository for interacting with the Doccano UserDetails API"""

    def __init__(self, client: BaseRepository):
        self._client = client