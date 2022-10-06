from __future__ import annotations

from enum import Enum
from typing import AbstractSet, Any, Dict, List, Mapping, Optional, Union

from pydantic import BaseModel
from pydantic.types import ConstrainedStr

IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
DictStrAny = Dict[str, Any]
MappingIntStrAny = Mapping[IntStr, Any]


class ProjectType(str, Enum):
    """Constants pointing to the types of project resource types"""

    DOCUMENT_CLASSIFICATION = "DocumentClassification"
    SEQUENCE_LABELING = "SequenceLabeling"
    SEQ2SEQ = "Seq2seq"
    SPEECH2TEXT = "Speech2text"
    IMAGE_CLASSIFICATION = "ImageClassification"
    BOUNDING_BOX = "BoundingBox"
    SEGMENTATION = "Segmentation"
    IMAGE_CAPTIONING = "ImageCaptioning"
    INTENT_DETECTION_AND_SLOT_FILLING = "IntentDetectionAndSlotFilling"


class Name(ConstrainedStr):
    min_length = 1
    max_length = 100
    strip_whitespace = True


class Description(ConstrainedStr):
    min_length = 1
    strip_whitespace = True


class Project(BaseModel):
    id: Optional[int]
    name: Name
    description: Description
    guideline: str = "Please write annotation guideline."
    project_type: ProjectType
    random_order: bool = False
    collaborative_annotation: bool = False
    single_class_classification: bool = False
    allow_overlapping: bool = False
    grapheme_mode: bool = False
    use_relation: bool = False
    tags: List[str] = []

    def dict(
        self,
        *,
        include: Union["AbstractSetIntStr", "MappingIntStrAny"] = None,
        exclude: Union["AbstractSetIntStr", "MappingIntStrAny"] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> "DictStrAny":
        attrs = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        attrs["resourcetype"] = self.resource_type
        attrs["project_type"] = self.project_type.value
        return attrs

    @property
    def resource_type(self) -> str:
        PROJECT_TO_RESOURCE_TYPE = {
            ProjectType.DOCUMENT_CLASSIFICATION: "TextClassificationProject",
            ProjectType.SEQUENCE_LABELING: "SequenceLabelingProject",
            ProjectType.SEQ2SEQ: "Seq2seqProject",
            ProjectType.SPEECH2TEXT: "Speech2textProject",
            ProjectType.IMAGE_CLASSIFICATION: "ImageClassificationProject",
            ProjectType.BOUNDING_BOX: "BoundingBoxProject",
            ProjectType.SEGMENTATION: "SegmentationProject",
            ProjectType.IMAGE_CAPTIONING: "ImageCaptioningProject",
            ProjectType.INTENT_DETECTION_AND_SLOT_FILLING: "IntentDetectionAndSlotFillingProject",
        }
        return PROJECT_TO_RESOURCE_TYPE[self.project_type]
