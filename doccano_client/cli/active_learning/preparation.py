import os
import pathlib
from typing import List

import spacy
from flair.data import Sentence, Token
from flair.datasets import ColumnCorpus
from spacy.training import offsets_to_biluo_tags

from doccano_client import DoccanoClient
from doccano_client.models.example import Example
from doccano_client.models.label import Span

from .models import Examples, NERDataset

DOCCANO_HOME = pathlib.Path(os.path.expanduser(os.environ.get("DOCCANO_HOME", "~/doccano")))


class UnlabeledDataset:
    def __init__(self):
        self.items = []

    @property
    def sentences(self):
        return [sentence for _, sentence in self.items]

    @property
    def ids(self):
        return [example_id for example_id, _ in self.items]

    def add(self, example: Example, sentence: Sentence):
        self.items.append((example.id, sentence))


def download_dataset(client: DoccanoClient, project_id: int) -> NERDataset:
    dataset_dir = DOCCANO_HOME / str(project_id) / "dataset"
    if not dataset_dir.exists():
        print(f"Downloading dataset for project {project_id}")
        dataset_dir.mkdir(parents=True, exist_ok=True)
        examples = Examples(client.list_examples(project_id))
        dataset = NERDataset(examples)
        dataset.save(dataset_dir)
    else:
        print(f"Loading dataset for project {project_id}")
        dataset = NERDataset.load(dataset_dir)

    for example in client.list_examples(project_id, is_confirmed=True):
        if not dataset.has_spans(example.id):
            spans = client.list_spans(project_id, example.id)  # type: ignore
            dataset.add_spans(example.id, spans)
            dataset.confirm(example.id)
    dataset.save(dataset_dir)
    return dataset


def make_nlp(lang: str = "en"):
    if lang == "cz":
        lang = "cs"
    nlp = spacy.blank(lang)
    return nlp


def prepare_datasets(client: DoccanoClient, project_id: int, lang: str = "en"):
    # download dataset
    dataset = download_dataset(client, project_id)

    # split train/test dataset
    train_dataset, test_dataset = dataset.labeled.split()

    # convert dataset to conll format
    nlp = make_nlp(lang)
    save_dir = DOCCANO_HOME / str(project_id) / "dataset"
    export_examples_to_conll(nlp, train_dataset, save_dir / "train.txt")
    export_examples_to_conll(nlp, test_dataset, save_dir / "test.txt")

    # load datasets for flair
    labeled_dataset = load_labeled_dataset(save_dir)
    unlabeled_dataset = load_unlabeled_dataset(nlp, dataset.unlabeled)
    return labeled_dataset, unlabeled_dataset


def convert_example_to_conll(nlp: spacy.Language, example: Example, spans: List[Span]):
    doc = nlp(example.text)  # type: ignore
    ents = [span.to_tuple() for span in spans]
    tags = offsets_to_biluo_tags(doc, ents)  # type: ignore
    for token, tag in zip(doc, tags):
        tag = tag.replace("U-", "S-")
        tag = tag.replace("L-", "E-")
        yield f"{token.text}\t{tag}\n"


def export_examples_to_conll(nlp: spacy.Language, dataset: NERDataset, path: pathlib.Path):
    with path.open("w", encoding="utf-8") as f:
        for example, spans in dataset:
            lines = convert_example_to_conll(nlp, example, spans)
            f.writelines(lines)
            f.write("\n")


def load_labeled_dataset(data_dir: pathlib.Path):
    columns = {0: "text", 1: "ner"}
    corpus = ColumnCorpus(
        data_dir,
        columns,
        train_file="train.txt",
        dev_file="test.txt",
        test_file="test.txt",
    )
    return corpus


def load_unlabeled_dataset(nlp: spacy.Language, dataset: NERDataset):
    unlabeled_dataset = UnlabeledDataset()
    for example, _ in dataset:
        doc = nlp(example.text)  # type: ignore
        sentence = Sentence()
        for word in doc:
            token = Token(text=word.text, start_position=word.idx, whitespace_after=word.whitespace_)
            token.add_tag("ner", "O")
            sentence.add_token(token)
        unlabeled_dataset.add(example, sentence)
    return unlabeled_dataset
