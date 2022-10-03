from typing import List

from doccano_client.models.role import Role
from doccano_client.repositories.role import RoleRepository


class RoleUseCase:
    def __init__(self, repository: RoleRepository):
        self._repository = repository

    def list(self) -> List[Role]:
        """Return all roles

        Returns:
            List[Role]: The list of the roles.
        """
        return self._repository.list()
