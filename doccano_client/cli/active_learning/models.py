import json
import pathlib
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

from sklearn.model_selection import train_test_split

from doccano_client.models.example import Example
from doccano_client.models.label import Span


class Examples:
    filename = "examples.json"

    def __init__(self, examples: Iterable[Example] = None):
        if examples is None:
            examples = []
        self.items = {int(example.id): example for example in examples if example.id}

    def __getitem__(self, example_id: Optional[int]) -> Example:
        if example_id is None:
            raise ValueError("Example ID is None.")
        return self.items[example_id]

    @property
    def ids(self) -> List[int]:
        return list(self.items.keys())

    def save(self, project_dir: pathlib.Path):
        path = project_dir / self.filename
        with path.open("w") as f:
            examples = [example.dict() for example in self.items.values()]
            json.dump(examples, f)

    @classmethod
    def load(cls, project_dir: pathlib.Path):
        path = project_dir / cls.filename
        if not path.exists():
            return cls()
        with path.open() as f:
            items = [Example.parse_obj(example) for example in json.load(f)]
        examples = cls(items)
        return examples

    def confirm(self, example_id: Optional[int]):
        if example_id is None:
            return
        self.items[example_id].is_confirmed = True

    def filter_by(self, is_confirmed: bool) -> "Examples":
        return Examples(example for example in self.items.values() if example.is_confirmed == is_confirmed)

    def filter_by_ids(self, ids: Iterable[int]) -> "Examples":
        return Examples(self.items[example_id] for example_id in ids)


class Spans:
    filename = "spans.json"

    def __init__(self, spans: Dict[int, List[Span]] = None):
        self.items = spans or {}

    def __contains__(self, example_id: Optional[int]) -> bool:
        if example_id is None:
            return False
        return example_id in self.items

    def __getitem__(self, example_id: Optional[int]) -> List[Span]:
        if example_id is None:
            raise ValueError("Example ID is None.")
        if example_id not in self.items:
            return []
        return self.items[example_id]

    def add(self, example_id: Optional[int], spans: List[Span]):
        if example_id is None:
            return
        self.items[example_id] = spans

    def save(self, project_dir: pathlib.Path):
        path = project_dir / self.filename
        with path.open("w") as f:
            spans = {example_id: [span.dict() for span in spans] for example_id, spans in self.items.items()}
            json.dump(spans, f)

    @classmethod
    def load(cls, project_dir: pathlib.Path):
        path = project_dir / cls.filename
        if not path.exists():
            return cls()
        with path.open() as f:
            items = json.load(f)
        items = {int(example_id): [Span.parse_obj(span) for span in spans] for example_id, spans in items.items()}
        spans = cls(items)
        return spans

    def filter_by(self, example_ids: List[int]) -> "Spans":
        return Spans({example_id: self.items[example_id] for example_id in example_ids})


class NERDataset:
    def __init__(self, examples: Examples = None, spans: Spans = None):
        self.examples = examples or Examples()
        self.spans = spans or Spans()

    def __iter__(self) -> Iterator[Tuple[Example, List[Span]]]:
        for example_id in self.examples.ids:
            yield self.examples[example_id], self.spans[example_id]

    def split(self, test_size: float = 0.2, random_state: int = 42) -> Iterable["NERDataset"]:
        train_ids, test_ids = train_test_split(self.examples.ids, test_size=test_size, random_state=random_state)
        train_examples = self.examples.filter_by_ids(train_ids)
        train_spans = self.spans.filter_by(train_ids)
        test_examples = self.examples.filter_by_ids(test_ids)
        test_spans = self.spans.filter_by(test_ids)
        return NERDataset(train_examples, train_spans), NERDataset(test_examples, test_spans)

    def save(self, project_dir: pathlib.Path):
        self.examples.save(project_dir)
        self.spans.save(project_dir)

    @classmethod
    def load(cls, project_dir: pathlib.Path):
        examples = Examples.load(project_dir)
        spans = Spans.load(project_dir)
        return cls(examples, spans)

    def add_spans(self, example_id: Optional[int], spans: List[Span]):
        if example_id is None:
            return
        self.spans.add(example_id, spans)

    def has_spans(self, example_id: Optional[int]) -> bool:
        if example_id is None:
            return False
        return example_id in self.spans

    def confirm(self, example_id: Optional[int]):
        if example_id is None:
            return
        self.examples.confirm(example_id)

    @property
    def labeled(self) -> "NERDataset":
        examples = self.examples.filter_by(is_confirmed=True)
        spans = self.spans.filter_by(examples.ids)
        return NERDataset(examples, spans)

    @property
    def unlabeled(self) -> "NERDataset":
        return NERDataset(self.examples.filter_by(is_confirmed=False))
