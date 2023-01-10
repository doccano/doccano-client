from .annotations import (
    Annotation,
    CategoryAnnotation,
    SpanAnnotation,
    TextLabelAnnotation,
)
from .category import Category
from .category_type import CategoryType
from .comments import Comment
from .examples import Document, Example
from .labels import LABEL_COLOR_CYCLE, Label
from .members import Member
from .projects import Project, ProjectTypes
from .relation import Relation
from .relation_type import RelationType
from .span import Span
from .span_type import SpanType
from .text import Text

__all__ = [
    "Annotation",
    "Category",
    "CategoryAnnotation",
    "CategoryType",
    "Comment",
    # TODO: Retained for backwards compatibility. Remove in v1.6.0
    "Document",
    # END TODO
    "Example",
    "Label",
    "LABEL_COLOR_CYCLE",
    "Member",
    "ProjectTypes",
    "Project",
    "Relation",
    "RelationType",
    "Span",
    "SpanAnnotation",
    "SpanType",
    "Text",
    "TextLabelAnnotation",
]
