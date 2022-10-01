from __future__ import annotations

import functools
from typing import List

from doccano_client.client import DoccanoClient
from doccano_client.models.label_type import LabelType


class LabelTypeClient:
    """Client for interacting with the Doccano label type API"""

    def __init__(self, client: DoccanoClient, resource_type="label-type"):
        self._client = client
        self._resource_type = resource_type

    def find_by_id(self, project_id: int, label_type_id: int) -> LabelType:
        """Find a label type by id

        Args:
            project_id (int): The id of the project
            label_type_id (int): The id of the label type to find

        Returns:
            LabelType: The found label type
        """
        response = self._client.get(f"projects/{project_id}/{self._resource_type}s/{label_type_id}")
        return LabelType.parse_obj(response.json())

    def list(self, project_id: int) -> List[LabelType]:
        """Return all label types in which you are a member

        Args:
            project_id (int): The id of the project

        Returns:
            LabelType: The list of the label types.
        """
        response = self._client.get(f"projects/{project_id}/{self._resource_type}s")
        label_types = [LabelType.parse_obj(label_type) for label_type in response.json()]
        return label_types

    def create(self, project_id: int, label_type: LabelType) -> LabelType:
        """Create a new label type

        Args:
            project_id (int): The id of the project
            label_type (LabelType): The label type to create

        Returns:
            LabelType: The created label type
        """
        response = self._client.post(f"projects/{project_id}/{self._resource_type}s", **label_type.dict(exclude={"id"}))
        return LabelType.parse_obj(response.json())

    def update(self, project_id: int, label_type: LabelType) -> LabelType:
        """Update a label type

        Args:
            project_id (int): The id of the project
            label_type (LabelType): The label type to update

        Returns:
            LabelType: The updated label type

        Raises:
            ValueError: If the label_type id is not set
        """
        if label_type.id is None:
            raise ValueError("label_type id must be set")
        resource = f"projects/{project_id}/{self._resource_type}s/{label_type.id}"
        response = self._client.put(resource, **label_type.dict())
        return LabelType.parse_obj(response.json())

    def delete(self, project_id: int, label_type: LabelType | int):
        """Delete a label type

        Args:
            project_id (int): The id of the project
            label_type (LabelType | int): The label type to delete

        Raises:
            ValueError: If the label_type id is not set
        """
        label_type_id = label_type if isinstance(label_type, int) else label_type.id
        if label_type_id is None:
            raise ValueError("label_type id must be set")
        resource = f"projects/{project_id}/{self._resource_type}s/{label_type_id}"
        self._client.delete(resource)

    def bulk_delete(self, project_id: int, label_types: List[int | LabelType]):
        """Bulk delete label types

        Args:
            project_id (int): The id of the project
            label_types (List[int | LabelType]): The list of label type ids to delete
        """
        ids = [label_type if isinstance(label_type, int) else label_type.id for label_type in label_types]
        self._client.delete(f"projects/{project_id}/{self._resource_type}s", **{"ids": ids})

    def upload(self, project_id: int, file_path: str):
        """Upload a label type

        Args:
            project_id (int): The id of the project
            file_path (str): The path to the file to upload
        """
        self._client.upload(f"projects/{project_id}/{self._resource_type}-upload", file_path)


CategoryTypeClient = functools.partial(LabelTypeClient, resource_type="category-type")
SpanTypeClient = functools.partial(LabelTypeClient, resource_type="span-type")
RelationTypeClient = functools.partial(LabelTypeClient, resource_type="relation-type")