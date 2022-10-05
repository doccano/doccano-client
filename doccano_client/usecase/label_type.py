from __future__ import annotations

from typing import List, Optional

from doccano_client.models.label_type import PREFIX_KEY, SUFFIX_KEY, LabelType
from doccano_client.repositories.label_type import LabelTypeRepository
from doccano_client.services.label_type import LabelTypeService


class LabelTypeUseCase:
    def __init__(self, repository: LabelTypeRepository, service: LabelTypeService):
        self._repository = repository
        self._service = service

    def find_by_id(self, project_id: int, label_type_id: int) -> LabelType:
        """Find a label type by id

        Args:
            project_id (int): The id of the project to find
            label_type_id (int): The id of the label type to find

        Returns:
            LabelType: The found label type
        """
        return self._repository.find_by_id(project_id, label_type_id)

    def list(self, project_id: int) -> List[LabelType]:
        """Return all label types

        Args:
            project_id (int): The id of the project

        Returns:
            List[LabelType]: The label types in the project.
        """
        return self._repository.list(project_id)

    def create(
        self,
        project_id: int,
        text: str,
        prefix_key: PREFIX_KEY = None,
        suffix_key: SUFFIX_KEY = None,
        color: Optional[str] = None,
    ) -> LabelType:
        """Create a new label type

        Args:
            project_id (int): The id of the project
            text (str): The text of the label type
            prefix_key (PREFIX_KEY): The prefix key of the label type
            suffix_key (SUFFIX_KEY): The suffix key of the label type
            color (str): The color of the label type

        Returns:
            LabelType: The created label type

        Raises:
            ValueError: If the label type already exists
        """
        label_type = LabelType.create(text=text, prefix_key=prefix_key, suffix_key=suffix_key, color=color)
        if self._service.exists(project_id, label_type):
            raise ValueError("The label type already exists")
        return self._repository.create(project_id, label_type)

    def update(
        self,
        project_id: int,
        label_type_id: int,
        text: str = None,
        prefix_key: PREFIX_KEY | int = -1,
        suffix_key: SUFFIX_KEY | int = -1,
        color: str = None,
    ) -> LabelType:
        """Update a label type

        Args:
            project_id (int): The id of the project
            label_type_id (int): The id of the label type
            text (str): The text of the label type
            prefix_key (PREFIX_KEY): The prefix key of the label type
            suffix_key (SUFFIX_KEY): The suffix key of the label type
            color (str): The color of the label type

        Returns:
            LabelType: The updated label type

        Raises:
            ValueError: If the label type already exists
        """
        label_type = self._repository.find_by_id(project_id, label_type_id)
        label_type = LabelType(
            id=label_type.id,
            text=text or label_type.text,
            prefix_key=prefix_key if prefix_key != -1 else label_type.prefix_key,
            suffix_key=suffix_key if suffix_key != -1 else label_type.suffix_key,
            background_color=color or label_type.background_color,
        )
        if self._service.exists(project_id, label_type):
            raise ValueError("The label type already exists")
        return self._repository.update(project_id, label_type)

    def delete(self, project_id: int, label_type_id: int):
        """Delete a label type.

        Args:
            project_id (int): The project id.
            label_type_id (int): The label type id.
        """
        self._repository.delete(project_id, label_type_id)

    def bulk_delete(self, project_id: int, label_type_ids: List[int]):
        """Bulk delete label types

        Args:
            project_id (int): The id of the project
            label_type_ids (List[int]): The list of label type ids to delete
        """
        self._repository.bulk_delete(project_id, label_type_ids)

    def upload(self, project_id: int, file_path: str):
        """Upload a label type

        Args:
            project_id (int): The id of the project
            file_path (str): The path to the file to upload
        """
        self._repository.upload(project_id, file_path)
