from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from doccano_client import DoccanoClient
from doccano_client.cli.active_learning.languages import LANGUAGES
from doccano_client.cli.estimators import select_estimator_class
from doccano_client.cli.usecases import build_annotator

DOCCANO_HOME = os.path.expanduser(os.environ.get("DOCCANO_HOME", "~/doccano"))
Path(DOCCANO_HOME).mkdir(parents=True, exist_ok=True)
base = os.path.abspath(os.path.dirname(__file__))
sys.path.append(base)
parser = argparse.ArgumentParser(description="doccano CLI.")


def command_login(args) -> DoccanoClient:
    credentials_path = Path(DOCCANO_HOME) / "credentials.json"

    # If credentials are given as arguments, try to use them.
    if "host" in args and "username" in args and "password" in args and args.host and args.username and args.password:
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


def command_predict(args):
    client = command_login(args)
    estimator = select_estimator_class(args.task, args.framework)(args.model)
    annotator = build_annotator(args.task, client, estimator)
    annotator.annotate(args.project, args.mapping)
    client.logout()


def command_teach(args):
    from .active_learning.manager import execute_active_learning

    client = command_login(args)
    execute_active_learning(
        client,
        project_id=args.project,
        lang=args.lang,
        query_strategy_name=args.query_strategy,
        transformer_model=args.transformer_model,
        train_frequency=args.train_frequency,
        patience=args.patience,
    )
    client.logout()


def command_help(args):
    print(parser.parse_args([args.command, "--help"]))


def main():
    # Create a command line parser.
    subparsers = parser.add_subparsers()

    # Create a parser for login.
    parser_login = subparsers.add_parser("login", help="see `login -h`")
    parser_login.add_argument("--username", type=str, default="admin", help="username")
    parser_login.add_argument("--password", type=str, default="password", help="password")
    parser_login.add_argument("--host", type=str, default="http://127.0.0.1:8000", help="host address")
    parser_login.set_defaults(handler=command_login)

    # Create a parser for web server.
    parser_predict = subparsers.add_parser("predict", help="see `predict -h`")
    parser_predict.add_argument("--task", type=str, choices=["ner", "asr"], required=True, help="task name")
    parser_predict.add_argument("--project", type=int, required=True, help="project id")
    parser_predict.add_argument("--model", type=str, required=True, help="model path")
    parser_predict.add_argument("--mapping", type=str, required=False, help="mapping file for label type")
    parser_predict.add_argument("--framework", default="spacy", choices=["spacy"], help="framework to predict output")
    parser_predict.set_defaults(handler=command_predict)

    # Create a parser for active learning
    parser_teach = subparsers.add_parser("teach", help="see `teach -h`")
    parser_teach.add_argument("--task", type=str, choices=["ner"], required=True, help="task name")
    parser_teach.add_argument("--project", type=int, required=True, help="project id")
    parser_teach.add_argument("--lang", type=str, choices=LANGUAGES, default="en", required=True, help="language code")
    parser_teach.add_argument(
        "--query_strategy",
        type=str,
        choices=["LC", "MNLP"],
        default="MNLP",
        required=True,
        help="query strategy. LC is least confidence, MNLP is maximum normalized log-probability.",
    )
    parser_teach.add_argument(
        "--transformer_model", type=str, required=False, help="transformer model name(e.g. bert-base-uncased)"
    )
    parser_teach.add_argument(
        "--train_frequency",
        type=int,
        default=50,
        help="How often to train during annotation (number of confirmed examples)",
    )
    parser_teach.add_argument(
        "--patience",
        type=int,
        default=-1,
        help="The number of training with no improvement",
    )
    parser_teach.set_defaults(handler=command_teach)

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
