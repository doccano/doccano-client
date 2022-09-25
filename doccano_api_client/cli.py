from __future__ import annotations

import abc
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Iterable, Iterator

from tqdm import tqdm

from doccano_api_client.beta import DoccanoClient
from doccano_api_client.beta.controllers.project import ProjectController
from doccano_api_client.beta.models.span import Span

DOCCANO_HOME = os.path.expanduser(os.environ.get("DOCCANO_HOME", "~/doccano"))
Path(DOCCANO_HOME).mkdir(parents=True, exist_ok=True)
base = os.path.abspath(os.path.dirname(__file__))
sys.path.append(base)
parser = argparse.ArgumentParser(description="doccano CLI.")


class Entity:
    def __init__(self, start_char: int, end_char: int, label: str):
        if start_char < 0 or end_char < 0:
            raise ValueError("The offset must be greater than or equal to 0")
        if start_char >= end_char:
            raise ValueError("The start offset must be less than the end offset")
        if label == "":
            raise ValueError("The label text must not be empty text.")
        self.start_char = start_char
        self.end_char = end_char
        self.label = label


class SpaCyEntityEstimator:
    def __init__(self, model: str):
        import spacy

        self.nlp = spacy.load(model)

    def predict(self, text: str) -> Iterator[Entity]:
        doc = self.nlp(text)
        for entity in doc.ents:
            yield Entity(start_char=entity.start_char, end_char=entity.end_char, label=entity.label_)


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


def command_login(args) -> DoccanoClient:
    credentials_path = Path(DOCCANO_HOME) / "credentials.json"

    # If credentials are given as arguments, try to use them.
    if args.host and args.username and args.password:
        client = DoccanoClient(args.host)
        client.login(args.username, args.password)
        with credentials_path.open(mode="w", encoding="utf-8") as f:
            credentials = {"host": args.host, "username": args.username, "password": args.password}
            json.dump(credentials, f)
        return client

    # If credentials are not given, try to load from the file.
    if credentials_path.exists():
        credentials = json.load(credentials_path.open(encoding="utf-8"))
        client = DoccanoClient(credentials["host"])
        client.login(credentials["username"], credentials["password"])
        return client
    raise ValueError("Any credentials are not given.")


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


def select_estimator_class(task: str, framework: str):
    if task == "ner" and framework == "spacy":
        return SpaCyEntityEstimator
    raise ValueError("There is no estimator.")


def build_annotator(task: str, project: ProjectController, estimator) -> LabelAnnotator:
    if task == "ner":
        return SpanAnnotator(project, estimator)
    raise ValueError("There is no annotator.")


def command_predict(args):
    client = command_login(args)
    project = client.projects.get(project_id=args.project)
    estimator = select_estimator_class(args.task, args.framework)(args.model)
    annotator = build_annotator(args.task, project, estimator)
    annotator.annotate(args.mapping)


def command_help(args):
    print(parser.parse_args([args.command, "--help"]))


def main():
    # Create a command line parser.
    subparsers = parser.add_subparsers()

    # Create a parser for login.
    parser_login = subparsers.add_parser("login", help="see `login -h`")
    parser_login.add_argument("--username", type=str, default="admin", help="username")
    parser_login.add_argument("--password", type=str, default="password", help="password")
    parser_login.add_argument("--host", type=str, default="localhost:8000", help="host address")
    parser_login.set_defaults(handler=command_login)

    # Create a parser for web server.
    parser_predict = subparsers.add_parser("predict", help="see `predict -h`")
    parser_predict.add_argument("--task", type=str, choices=["ner"], required=True, help="task name")
    parser_predict.add_argument("--project", type=int, required=True, help="project id")
    parser_predict.add_argument("--model", type=str, required=True, help="model path")
    parser_predict.add_argument("--mapping", type=str, required=False, help="mapping file for label type")
    parser_predict.add_argument("--framework", default="spacy", choices=["spacy"], help="framework to predict output")
    parser_predict.set_defaults(handler=command_predict)

    # Create a parser for help.
    parser_help = subparsers.add_parser("help", help="see `help -h`")
    parser_help.add_argument("command", help="command name which help is shown")
    parser_help.set_defaults(handler=command_help)

    # Dispatch handler.
    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        # If specified unknown command, show help.
        parser.print_help()


if __name__ == "__main__":
    main()
