from __future__ import annotations

from typing import Generic, List, Optional, TypeVar

from doccano_client.models.label import (
    BoundingBox,
    Category,
    Label,
    Relation,
    Segment,
    Span,
    Text,
)
from doccano_client.repositories.label import LabelRepository
from doccano_client.repositories.label_type import LabelTypeRepository

T = TypeVar("T", bound=Label)


class LabelUseCase(Generic[T]):
    def __init__(self, repository: LabelRepository, label_type_repository: LabelTypeRepository = None):
        self._repository = repository
        self._label_type_repository = label_type_repository

    def find_by_id(self, project_id: int, example_id: int, label_id: int) -> T:
        """Find a label by id

        Args:
            project_id (int): The id of the project to find
            example_id (int): The id of the example
            label_id (int): The id of the label to find

        Returns:
            T: The found label
        """
        return self._repository.find_by_id(project_id, example_id, label_id)

    def list(self, project_id: int, example_id: int) -> List[T]:
        """Return all labels

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example

        Returns:
            T: The labels in the project.
        """
        return self._repository.list(project_id, example_id)

    def delete(self, project_id: int, example_id: int, label_id: int):
        """Delete a label.

        Args:
            project_id (int): The project id
            example_id (int): The id of the example
            label_id (int): The label id
        """
        label = self.find_by_id(project_id, example_id, label_id)
        self._repository.delete(project_id, label)

    def delete_all(self, project_id: int, example_id: int):
        """Delete all labels

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
        """
        self._repository.delete_all(project_id, example_id)


class CategoryUseCase(LabelUseCase[Category]):
    def create(
        self, project_id: int, example_id: int, label: int | str, human_annotated=False, confidence=0.0
    ) -> Category:
        """Create a new category label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Category: The created category label

        Raises:
            ValueError: If the label type repository is not set
        """
        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id  # type: ignore

        category = Category(example=example_id, label=label, manual=human_annotated, prob=confidence)
        return self._repository.create(project_id, category)

    def update(
        self,
        project_id: int,
        example_id: int,
        label_id: int,
        label: Optional[int | str] = None,
        human_annotated: bool = None,
        confidence: float = None,
    ) -> Category:
        """Update a category label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            label_id (int): The id of the label
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Category: The updated category label

        Raises:
            ValueError: If the label type repository is not set
        """
        category = self.find_by_id(project_id, example_id, label_id)

        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id  # type: ignore

        category = Category(
            id=category.id,
            example=example_id,
            label=label or category.label,
            manual=human_annotated or category.manual,
            prob=confidence or category.prob,
        )
        return self._repository.update(project_id, category)


class SpanUseCase(LabelUseCase[Span]):
    def create(
        self,
        project_id: int,
        example_id: int,
        start_offset: int,
        end_offset: int,
        label: int | str,
        human_annotated: bool = False,
        confidence: float = 0.0,
    ) -> Span:
        """Create a new span label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            start_offset (int): The start offset of the span
            end_offset (int): The end offset of the span
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Span: The created span label

        Raises:
            ValueError: If the label type repository is not set
        """
        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id  # type: ignore

        span = Span(
            example=example_id,
            start_offset=start_offset,
            end_offset=end_offset,
            label=label,
            manual=human_annotated,
            prob=confidence,
        )
        return self._repository.create(project_id, span)

    def update(
        self,
        project_id: int,
        example_id: int,
        label_id: int,
        start_offset: Optional[int] = None,
        end_offset: Optional[int] = None,
        label: Optional[int | str] = None,
        human_annotated: bool = None,
        confidence: float = None,
    ) -> Span:
        """Update a span label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            label_id (int): The id of the label
            start_offset (int): The start offset of the span
            end_offset (int): The end offset of the span
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Span: The updated span label

        Raises:
            ValueError: If the label type repository is not set
        """
        span = self.find_by_id(project_id, example_id, label_id)

        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id

        span = Span(
            id=span.id,
            example=example_id,
            start_offset=start_offset or span.start_offset,
            end_offset=end_offset or span.end_offset,
            label=label or span.label,
            manual=human_annotated or span.manual,
            prob=confidence or span.prob,
        )
        return self._repository.update(project_id, span)


class RelationUseCase(LabelUseCase[Relation]):
    def create(
        self,
        project_id: int,
        example_id: int,
        from_id: int,
        to_id: int,
        label: int | str,
        human_annotated: bool = False,
        confidence: float = 0.0,
    ) -> Relation:
        """Create a new relation label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            from_id (int): The id of the from span
            to_id (int): The id of the to span
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Relation: The created relation label

        Raises:
            ValueError: If the label type repository is not set
        """
        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id  # type: ignore

        relation = Relation(
            example=example_id,
            from_id=from_id,
            to_id=to_id,
            type=label,
            manual=human_annotated,
            prob=confidence,
        )
        return self._repository.create(project_id, relation)

    def update(
        self,
        project_id: int,
        example_id: int,
        label_id: int,
        from_id: Optional[int] = None,
        to_id: Optional[int] = None,
        label: Optional[int | str] = None,
        human_annotated: bool = None,
        confidence: float = None,
    ) -> Relation:
        """Update a relation label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            label_id (int): The id of the label
            from_id (int): The id of the from span
            to_id (int): The id of the to span
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Relation: The updated relation label

        Raises:
            ValueError: If the label type repository is not set
        """
        relation = self.find_by_id(project_id, example_id, label_id)

        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id

        relation = Relation(
            id=relation.id,
            example=example_id,
            from_id=from_id or relation.from_id,
            to_id=to_id or relation.to_id,
            type=label or relation.type,
            manual=human_annotated or relation.manual,
            prob=confidence or relation.prob,
        )
        return self._repository.update(project_id, relation)


class TextUseCase(LabelUseCase[Text]):
    def create(
        self,
        project_id: int,
        example_id: int,
        text: str,
        human_annotated: bool = False,
        confidence: float = 0.0,
    ) -> Text:
        """Create a new text label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            text (str): The text to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Text: The created text label
        """
        text_label = Text(
            example=example_id,
            text=text,
            manual=human_annotated,
            prob=confidence,
        )
        return self._repository.create(project_id, text_label)

    def update(
        self,
        project_id: int,
        example_id: int,
        label_id: int,
        text: Optional[str] = None,
        human_annotated: bool = None,
        confidence: float = None,
    ) -> Text:
        """Update a text label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            label_id (int): The id of the label
            text (str): The text to update
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Text: The updated text label
        """
        text_label = self.find_by_id(project_id, example_id, label_id)
        text_label = Text(
            id=text_label.id,
            example=example_id,
            text=text or text_label.text,
            manual=human_annotated or text_label.manual,
            prob=confidence or text_label.prob,
        )
        return self._repository.update(project_id, text_label)


class BoundingBoxUseCase(LabelUseCase[BoundingBox]):
    def create(
        self,
        project_id: int,
        example_id: int,
        x: float,
        y: float,
        width: float,
        height: float,
        label: int | str,
        human_annotated: bool = False,
        confidence: float = 0.0,
    ) -> BoundingBox:
        """Create a new bounding box label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            x (float): The x coordinate of the bounding box
            y (float): The y coordinate of the bounding box
            width (float): The width of the bounding box
            height (float): The height of the bounding box
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            BoundingBox: The created bounding box label

        Raises:
            ValueError: If the label type repository is not set
        """
        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id  # type: ignore

        bounding_box = BoundingBox(
            example=example_id,
            x=x,
            y=y,
            width=width,
            height=height,
            label=label,
            manual=human_annotated,
            prob=confidence,
        )
        return self._repository.create(project_id, bounding_box)

    def update(
        self,
        project_id: int,
        example_id: int,
        label_id: int,
        x: Optional[float] = None,
        y: Optional[float] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
        label: Optional[int | str] = None,
        human_annotated: bool = None,
        confidence: float = None,
    ) -> BoundingBox:
        """Update a bounding box label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            label_id (int): The id of the label
            x (float): The x coordinate of the bounding box
            y (float): The y coordinate of the bounding box
            width (float): The width of the bounding box
            height (float): The height of the bounding box
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            BoundingBox: The updated bounding box label

        Raises:
            ValueError: If the label type repository is not set
        """
        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        bounding_box = self.find_by_id(project_id, example_id, label_id)

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id

        bounding_box = BoundingBox(
            id=bounding_box.id,
            example=example_id,
            x=x or bounding_box.x,
            y=y or bounding_box.y,
            width=width or bounding_box.width,
            height=height or bounding_box.height,
            label=label or bounding_box.label,
            manual=human_annotated or bounding_box.manual,
            prob=confidence or bounding_box.prob,
        )
        return self._repository.update(project_id, bounding_box)


class SegmentUseCase(LabelUseCase[Segment]):
    def create(
        self,
        project_id: int,
        example_id: int,
        points: List[float],
        label: int | str,
        human_annotated: bool = False,
        confidence: float = 0.0,
    ) -> Segment:
        """Create a new segment label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            points (List[float]): The points of the segment
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Segment: The created segment label

        Raises:
            ValueError: If the label type repository is not set
        """
        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id  # type: ignore

        segment = Segment(
            example=example_id,
            points=points,
            label=label,
            manual=human_annotated,
            prob=confidence,
        )
        return self._repository.create(project_id, segment)

    def update(
        self,
        project_id: int,
        example_id: int,
        label_id: int,
        points: Optional[List[float]] = None,
        label: Optional[int | str] = None,
        human_annotated: bool = None,
        confidence: float = None,
    ) -> Segment:
        """Update a segment label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            label_id (int): The id of the label
            points (List[float]): The points of the segment
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Segment: The updated segment label

        Raises:
            ValueError: If the label type repository is not set
        """
        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        segment = self.find_by_id(project_id, example_id, label_id)

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id

        segment = Segment(
            id=segment.id,
            example=example_id,
            points=points or segment.points,
            label=label or segment.label,
            manual=human_annotated or segment.manual,
            prob=confidence or segment.prob,
        )
        return self._repository.update(project_id, segment)
