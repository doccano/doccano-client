from .annotation import AnnotationController, AnnotationsController
from .category import CategoriesController, CategoryController
from .category_type import CategoryTypeController, CategoryTypesController
from .comment import CommentController, CommentsController
from .example import (
    DocumentController,
    DocumentsController,
    ExampleController,
    ExamplesController,
)
from .label import LabelController, LabelsController
from .project import ProjectController, ProjectsController
from .relation import RelationController, RelationsController
from .relation_type import RelationTypeController, RelationTypesController
from .span import SpanController, SpansController
from .span_type import SpanTypeController, SpanTypesController
from .text import TextController, TextsController

__all__ = [
    "AnnotationController",
    "AnnotationsController",
    "CategoryController",
    "CategoriesController",
    "CategoryTypeController",
    "CategoryTypesController",
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
    "SpanController",
    "SpansController",
    "SpanTypeController",
    "SpanTypesController",
    "RelationController",
    "RelationsController",
    "RelationTypeController",
    "RelationTypesController",
    "TextController",
    "TextsController",
]
