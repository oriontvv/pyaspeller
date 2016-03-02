from __future__ import print_function

try:
    from unittest import mock
except ImportError:
    import mock

import pytest
from pyaspeller import create_args_parser, main, create_speller


@pytest.fixture()
def argparser():
    return create_args_parser()


@pytest.fixture()
def speller(argparser):
    args = argparser.parse_args([""])
    return create_speller(args)


def test_args_parser_version(capsys):
    version = '7.7.7'
    with mock.patch('pyaspeller.__version__', version):
        with pytest.raises(SystemExit):
            main()
            out, err = capsys.readouterr()
            assert version in out, "Bad version: " + out


def test_default_speller(speller):
    assert speller.format == 'auto', 'Bad default format: ' + speller.format
