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
]
