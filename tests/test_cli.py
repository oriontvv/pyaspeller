from __future__ import annotations
import pytest
from argparse import ArgumentParser

from pyaspeller import _create_args_parser, _create_speller, Speller


@pytest.fixture()
def argparser() -> ArgumentParser:
    return _create_args_parser()


@pytest.fixture()
def speller(argparser: ArgumentParser) -> Speller:
    args = argparser.parse_args([""])
    return _create_speller(args)


def test_default_speller(speller: Speller) -> None:
    assert speller.format == "plain", "Bad default format: " + speller.format
