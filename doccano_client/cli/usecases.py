from __future__ import annotations

import abc
import json
from typing import Dict, Iterator

from tqdm import tqdm

from doccano_client import DoccanoClient
from doccano_client.cli.entity import Entity


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
    def __init__(self, client: DoccanoClient, estimator):
        self.client = client
        self.estimator = estimator

    def annotate(self, project_id: int, filename: str = None):
        raise NotImplementedError()


class SpanAnnotator(LabelAnnotator):
    def annotate(self, project_id: int, filename: str = None):
        span_types = self.client.list_label_types(project_id, type="span")
        type_to_id: Dict[str, int] = {span_type.text: span_type.id for span_type in span_types}  # type: ignore
        mapping = load_mapping(filename) if filename else {}

        # predict label and post it.
        total = self.client.count_examples(project_id)
        examples = self.client.list_examples(project_id)
        for example in tqdm(examples, total=total):
            entities = self.estimator.predict(example.text)
            entities = self._convert_label_name(entities, mapping)
            # Todo: bulk create
            for entity in entities:
                if entity.label in type_to_id:
                    self.client.create_span(
                        project_id,
                        example.id,
                        start_offset=entity.start_char,
                        end_offset=entity.end_char,
                        label=type_to_id[entity.label],
                    )

    def _convert_label_name(self, entities: list[Entity], mapping: dict[str, str]) -> Iterator[Entity]:
        for entity in entities:
            if entity.label in mapping:
                entity.label = mapping[entity.label]
            yield entity


def build_annotator(task: str, client: DoccanoClient, estimator) -> LabelAnnotator:
    if task == "ner":
        return SpanAnnotator(client, estimator)
    raise ValueError("There is no annotator.")
