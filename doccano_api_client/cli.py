from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Iterator, TypedDict

from doccano_api_client.beta import DoccanoClient
from doccano_api_client.beta.controllers import ProjectsController
from doccano_api_client.beta.models.span import Span

DOCCANO_HOME = os.path.expanduser(os.environ.get("DOCCANO_HOME", "~/doccano"))
Path(DOCCANO_HOME).mkdir(parents=True, exist_ok=True)
base = os.path.abspath(os.path.dirname(__file__))
sys.path.append(base)
parser = argparse.ArgumentParser(description="doccano CLI.")


class Entity(TypedDict):
    start_char: int
    end_char: int
    label: str


class SpaCyPredictor:
    def __init__(self, model: str):
        import spacy

        self.nlp = spacy.load(model)

    def predict(self, text: str) -> Iterator[Entity]:
        doc = self.nlp(text)
        for entity in doc.ents:
            yield Entity(start_char=entity.start_char, end_char=entity.end_char, label=entity.label_)


class LabelMapper:
    def __init__(self, filepath: str, type_to_id: dict[str, int], encoding="utf-8"):
        self.mapping = self.load(filepath, encoding)
        self.type_to_id = type_to_id

    def load(self, filepath, encoding) -> dict[str, str]:
        with open(filepath, encoding=encoding) as f:
            mapping = json.load(f)
            if isinstance(mapping, dict):
                return mapping
            raise ValueError("Mapping should be dictionary.")

    def map(self, entity: Entity) -> Span:
        if entity["label"] in self.mapping:
            entity["label"] = self.mapping[entity["label"]]
        if entity["label"] in self.type_to_id:
            return Span(
                start_offset=entity["start_char"],
                end_offset=entity["end_char"],
                label=self.type_to_id[entity["label"]],
                prob=0,
            )
        raise ValueError(f"Label {entity['label']} is not defined in the project.")


def command_login(args) -> DoccanoClient:
    client = DoccanoClient(args.host)
    client.login(args.username, args.password)
    return client


def command_predict(args):
    # prepare the project.
    client = command_login(args)
    projects = ProjectsController(client.api_url, client.client_session)
    project = projects.get(project_id=args.project)

    # Todo: delegate function by the task.
    # prepare label types
    span_types = project.span_types.all()
    type_to_id = {span_type.span_type.text: span_type.id for span_type in span_types}

    # prepare the predictor.
    predictor = SpaCyPredictor(args.model)
    mapper = LabelMapper(args.mapping, type_to_id)

    # predict label and post it.
    for example in project.examples.all():
        entities = predictor.predict(example.example.text)
        spans = map(mapper.map, entities)
        for span in spans:
            example.spans.create(span)


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
    parser_predict.add_argument("--task", type=str, help="task name")
    parser_predict.add_argument("--project", type=int, help="project id")
    parser_predict.add_argument("--model", type=str, help="model path")
    parser_predict.add_argument("--mapping", type=str, help="mapping file for label type")
    parser_predict.add_argument("--framework", type=str, default="spacy", help="framework to predict output")
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
