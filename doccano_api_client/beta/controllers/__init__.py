from .annotation import AnnotationController, AnnotationsController
from .comment import CommentController, CommentsController
from .example import (
    DocumentController,
    DocumentsController,
    ExampleController,
    ExamplesController,
)
from .label import LabelController, LabelsController
from .project import ProjectController, ProjectsController
from .relation_type import RelationTypeController, RelationTypesController
from .span_type import SpanTypeController, SpanTypesController

__all__ = [
    "AnnotationController",
    "AnnotationsController",
    "CommentController",
    "CommentsController",
    # TODO: Retained for backwards compatibility. Remove in v1.6.0
    "DocumentController",
    "DocumentsController",
    # END TODO
    "ExampleController",
    "ExamplesController",
    "LabelController",
    "LabelsController",
    "ProjectController",
    "ProjectsController",
    "SpanTypeController",
    "SpanTypesController",
    "RelationTypeController",
    "RelationTypesController",
]
