import pytest
from pyaspeller import _create_args_parser, main, _create_speller


@pytest.fixture()
def argparser():
    return _create_args_parser()


@pytest.fixture()
def speller(argparser):
    args = argparser.parse_args([""])
    return _create_speller(args)


def test_default_speller(speller):
    assert speller.format == 'plain', 'Bad default format: ' + speller.format
