from enum import Enum
from typing import Any, Dict

from pydantic import BaseModel


class Option(BaseModel):
    task_id: str
    name: str
    display_name: str
    example: str
    accept_types: str
    properties: Dict[str, Any]


class Task(str, Enum):
    DOCUMENT_CLASSIFICATION = "DocumentClassification"
    SEQUENCE_LABELING = "SequenceLabeling"
    SEQ2SEQ = "Seq2seq"
    SPEECH2TEXT = "Speech2text"
    IMAGE_CLASSIFICATION = "ImageClassification"
    BOUNDING_BOX = "BoundingBox"
    SEGMENTATION = "Segmentation"
    IMAGE_CAPTIONING = "ImageCaptioning"
    INTENT_DETECTION_AND_SLOT_FILLING = "IntentDetectionAndSlotFilling"
    RELATION_EXTRACTION = "RelationExtraction"
