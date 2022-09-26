from typing import Sequence

import pytest
from _pytest.config import Config, argparsing
from _pytest.unittest import TestCaseFunction


def pytest_addoption(parser: argparsing.Parser) -> None:
    """Add specified option to pytest cli command."""
    parser.addoption(
        "--runintegrationtest",
        default=False,
        action="store_true",
        help="run local integration test",
    )


def pytest_configure(config: Config) -> None:
    """Add marker value in config. Goes in tandem with the pytest_addoption."""
    config.addinivalue_line("markers", "localintegrationtest: mark test as local integration test")


def pytest_collection_modifyitems(config: Config, items: Sequence[TestCaseFunction]) -> None:
    """Does not run tests marked as slow when the runslow option is set to true."""
    if config.getoption("--runintegrationtest"):
        # --runintegrationtest given in cli: do not skip integration tests
        return
    skip_slow = pytest.mark.skip(reason="need --runintegrationtest option to run")
    for item in items:
        if "localintegrationtest" in item.keywords:
            item.add_marker(skip_slow)
