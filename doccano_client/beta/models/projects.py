from dataclasses import dataclass, field
from typing import Dict, Type

from dataclasses_json import DataClassJsonMixin

from .annotations import (
    Annotation,
    CategoryAnnotation,
    SpanAnnotation,
    TextLabelAnnotation,
)


class ProjectTypes:
    """Constants pointing to the types of project resource types available for new projects"""

    DOCUMENT_CLASSIFICATION = "DocumentClassification"
    SEQUENCE_LABELING = "SequenceLabeling"
    SEQ2SEQ = "Seq2seq"


PROJECT_TO_RESOURCE_TYPE = {
    # For some reason, DocumentClassification's resource type on Doccano doesn't match up directly
    ProjectTypes.DOCUMENT_CLASSIFICATION: "TextClassificationProject",
    ProjectTypes.SEQUENCE_LABELING: "SequenceLabelingProject",
    ProjectTypes.SEQ2SEQ: "Seq2seqProject",
}


# Each project type is associated with a specific annotation type
PROJECT_TO_ANNOTATION_MODEL: Dict[str, Type[Annotation]] = {
    ProjectTypes.DOCUMENT_CLASSIFICATION: CategoryAnnotation,
    ProjectTypes.SEQUENCE_LABELING: SpanAnnotation,
    ProjectTypes.SEQ2SEQ: TextLabelAnnotation,
}


@dataclass
class Project(DataClassJsonMixin):
    name: str
    description: str
    project_type: str
    resourcetype: str = field(init=False)

    guideline: str = "Please write annotation guideline."
    random_order: bool = False
    collaborative_annotation: bool = False
    single_class_classification: bool = False
    allow_overlapping: bool = False
    grapheme_mode: bool = False
    use_relation: bool = False

    def __post_init__(self) -> None:
        """Propogates resourcetype field based on project_type field, needed for project creation"""
        if self.project_type not in PROJECT_TO_RESOURCE_TYPE:
            raise AssertionError(f"project_type not in: {PROJECT_TO_RESOURCE_TYPE.keys()}")
        self.resourcetype = PROJECT_TO_RESOURCE_TYPE.get(self.project_type, "NotAResource")

    def get_annotation_model(self) -> Type[Annotation]:
        """Return the appropriate Annotation type for this project type."""
        return PROJECT_TO_ANNOTATION_MODEL[self.project_type]
