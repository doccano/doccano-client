from __future__ import annotations

import abc
import json
from typing import Iterable, Iterator

from tqdm import tqdm

from doccano_api_client.beta.controllers import ProjectController
from doccano_api_client.beta.models import Span
from doccano_api_client.cli.entity import Entity


def load_mapping(filepath: str, encoding="utf-8") -> dict[str, str]:
    with open(filepath, encoding=encoding) as f:
        mapping = json.load(f)
        if not isinstance(mapping, dict):
            raise ValueError("Mapping must be dictionary.")
        if all(isinstance(key, str) for key in mapping.keys()):
            raise ValueError("Key must be string.")
        if all(isinstance(value, str) for value in mapping.values()):
            raise ValueError("Value must be string.")
        return mapping


class LabelAnnotator(abc.ABC):
    def __init__(self, project: ProjectController, estimator):
        self.project = project
        self.estimator = estimator

    def annotate(self, mapping):
        raise NotImplementedError()


class SpanAnnotator(LabelAnnotator):
    def annotate(self, filename: str | None):
        span_types = self.project.span_types.all()
        type_to_id = {span_type.span_type.text: span_type.id for span_type in span_types}
        mapping = load_mapping(filename) if filename else {}

        # predict label and post it.
        total = self.project.examples.count()
        for example in tqdm(self.project.examples.all(), total=total):
            entities = self.estimator.predict(example.example.text)
            entities = self._convert_label_name(entities, mapping)
            spans = self._convert_label_name_to_id(entities, type_to_id)
            # Todo: bulk create
            for span in spans:
                example.spans.create(span)

    def _convert_label_name(self, entities: list[Entity], mapping: dict[str, str]) -> Iterator[Entity]:
        for entity in entities:
            if entity.label in mapping:
                entity.label = mapping[entity.label]
            yield entity

    def _convert_label_name_to_id(self, entities: Iterable[Entity], type_to_id: dict[str, int]) -> Iterator[Span]:
        for entity in entities:
            if entity.label in type_to_id:
                yield Span(
                    start_offset=entity.start_char,
                    end_offset=entity.end_char,
                    label=type_to_id[entity.label],
                    prob=0,
                )


def build_annotator(task: str, project: ProjectController, estimator) -> LabelAnnotator:
    if task == "ner":
        return SpanAnnotator(project, estimator)
    raise ValueError("There is no annotator.")
