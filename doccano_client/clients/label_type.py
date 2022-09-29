from __future__ import annotations

from typing import List

from doccano_client.client import DoccanoClient
from doccano_client.models.label_type import LabelType


class LabelTypeClient:
    """Client for interacting with the Doccano label_type API"""

    resource_type = "label-type"

    def __init__(self, client: DoccanoClient):
        self._client = client

    def find_by_id(self, project_id: int, label_type_id: int) -> LabelType:
        """Find a label_type by id

        Args:
            project_id (int): The id of the project
            label_type_id (int): The id of the label_type to find
        """
        response = self._client.get(f"projects/{project_id}/{self.resource_type}s/{label_type_id}")
        return LabelType.parse_obj(response.json())

    def list(self, project_id: int) -> List[LabelType]:
        """Return all label_types in which you are a member

        Args:
            project_id (int): The id of the project

        Returns:
            LabelType: The list of the label_types.
        """
        response = self._client.get(f"projects/{project_id}/{self.resource_type}s")
        label_types = [LabelType.parse_obj(label_type) for label_type in response.json()]
        return label_types

    def create(self, project_id: int, label_type: LabelType) -> LabelType:
        """Create a new label_type

        Args:
            project_id (int): The id of the project
            label_type (LabelType): The label_type to create

        Returns:
            LabelType: The created label_type
        """
        response = self._client.post(f"projects/{project_id}/{self.resource_type}s", **label_type.dict(exclude={"id"}))
        return LabelType.parse_obj(response.json())

    def update(self, project_id: int, label_type: LabelType) -> LabelType:
        """Update a label_type

        Args:
            project_id (int): The id of the project
            label_type (LabelType): The label_type to update

        Returns:
            LabelType: The updated label_type
        """
        resource = f"projects/{project_id}/{self.resource_type}s/{label_type.id}"
        response = self._client.put(resource, **label_type.dict())
        return LabelType.parse_obj(response.json())

    def delete(self, project_id: int, label_type: LabelType | int):
        """Delete a label_type

        Args:
            project_id (int): The id of the project
            label_type (LabelType | int): The label_type to delete
        """
        label_type_id = label_type if isinstance(label_type, int) else label_type.id
        resource = f"projects/{project_id}/{self.resource_type}s/{label_type_id}"
        self._client.delete(resource)

    def bulk_delete(self, project_id: int, label_types: List[int | LabelType]):
        """Bulk delete label_types

        Args:
            project_id (int): The id of the project
            label_types (List[int | LabelType]): The list of label_type ids to delete
        """
        ids = [label_type if isinstance(label_type, int) else label_type.id for label_type in label_types]
        self._client.delete(f"projects/{project_id}/{self.resource_type}s", **{"ids": ids})

    def upload(self, project_id: int, file_path: str):
        """Upload a label_type

        Args:
            project_id (int): The id of the project
            file_path (str): The path to the file to upload
        """
        self._client.upload(f"projects/{project_id}/{self.resource_type}-upload", file_path)


class CategoryTypeClient(LabelTypeClient):
    """Client for interacting with the Doccano category_type API"""

    resource_type = "category-type"


class SpanTypeClient(LabelTypeClient):
    """Client for interacting with the Doccano span_type API"""

    resource_type = "span-type"


class RelationTypeClient(LabelTypeClient):
    """Client for interacting with the Doccano relation_type API"""

    resource_type = "relation-type"
