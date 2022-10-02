from __future__ import annotations

import functools
from typing import Generic, List, TypeVar

from doccano_client.client import DoccanoClient
from doccano_client.models.label import (
    BoundingBox,
    Category,
    Label,
    Relation,
    Segment,
    Span,
    Text,
)

T = TypeVar("T", bound=Label)


class LabelClient(Generic[T]):
    """Client for interacting with the Doccano label API"""

    def __init__(self, client: DoccanoClient, label_class: T, resource_type: str):
        self._client = client
        self._label_class = label_class
        self._resource_type = resource_type

    def find_by_id(self, project_id: int, example_id: int, label_id: int) -> T:
        """Find a label by id

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            label_id (int): The id of the label to find

        Returns:
            T: The found label
        """
        resource = f"projects/{project_id}/examples/{example_id}/{self._resource_type}/{label_id}"
        response = self._client.get(resource)
        return self._label_class.parse_obj(response.json())

    def list(self, project_id: int, example_id: int) -> List[T]:
        """Return all label in which you are a member

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example

        Returns:
            T: The list of the label.
        """
        resource = f"projects/{project_id}/examples/{example_id}/{self._resource_type}"
        response = self._client.get(resource)
        labels = [self._label_class.parse_obj(label) for label in response.json()]
        return labels

    def create(self, project_id: int, label: T) -> T:
        """Create a new label

        Args:
            project_id (int): The id of the project
            label (T): The label to create

        Returns:
            T: The created label
        """
        resource = f"projects/{project_id}/examples/{label.example}/{self._resource_type}"
        response = self._client.post(resource, json=label.dict(exclude={"id"}))
        return self._label_class.parse_obj(response.json())

    def update(self, project_id: int, label: T) -> T:
        """Update a label

        Args:
            project_id (int): The id of the project
            label (T): The label to update

        Returns:
            T: The updated label

        Raises:
            ValueError: If the label id is not set
        """
        if label.id is None:
            raise ValueError("Label id is required")
        resource = f"projects/{project_id}/examples/{label.example}/{self._resource_type}/{label.id}"
        response = self._client.put(resource, json=label.dict())
        return self._label_class.parse_obj(response.json())

    def delete(self, project_id: int, label: T | int):
        """Delete a label

        Args:
            project_id (int): The id of the project
            label (T | int): The label to delete

        Raises:
            ValueError: If the label id is not set
        """
        label_id = label if isinstance(label, int) else label.id
        if label_id is None:
            raise ValueError("Label id is required")
        resource = f"projects/{project_id}/examples/{label.example}/{self._resource_type}/{label_id}"
        self._client.delete(resource)

    def delete_all(self, project_id: int, example_id: int):
        """Delete all labels

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
        """
        resource = f"projects/{project_id}/examples/{example_id}/{self._resource_type}"
        self._client.delete(resource)


CategoryClient = functools.partial(LabelClient[Category], label_class=Category, resource_type="categories")
SpanClient = functools.partial(LabelClient[Span], label_class=Span, resource_type="spans")
RelationClient = functools.partial(LabelClient[Relation], label_class=Relation, resource_type="relations")
SegmentClient = functools.partial(LabelClient[Segment], label_class=Segment, resource_type="segments")
TextClient = functools.partial(LabelClient[Text], label_class=Text, resource_type="texts")
BoundingBoxClient = functools.partial(LabelClient[BoundingBox], label_class=BoundingBox, resource_type="bboxes")
