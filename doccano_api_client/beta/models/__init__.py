from .annotations import (
    Annotation,
    CategoryAnnotation,
    SpanAnnotation,
    TextLabelAnnotation,
)
from .comments import Comment
from .examples import Document, Example
from .labels import LABEL_COLOR_CYCLE, Label
from .projects import Project, ProjectTypes
from .relation import Relation
from .relation_type import RelationType
from .span import Span
from .span_type import SpanType

__all__ = [
    "Comment",
    # TODO: Retained for backwards compatibility. Remove in v1.6.0
    "Document",
    # END TODO
    "Example",
    "Label",
    "LABEL_COLOR_CYCLE",
    "ProjectTypes",
    "Project",
    "CategoryAnnotation",
    "SpanAnnotation",
    "TextLabelAnnotation",
    "Annotation",
    "Span",
    "SpanType",
    "RelationType",
    "Relation",
]
