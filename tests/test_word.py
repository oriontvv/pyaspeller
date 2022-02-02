import pytest
from pyaspeller.errors import BadArgumentError

from pyaspeller import Word


def test_correct_word():
    w = Word("test")
    assert w.correct
    assert not w.variants
    assert not w.spellsafe


def test_incorrect_word():
    w = Word("taxx")
    assert not w.correct
    assert w.variants == ["tax", "texx", "tixx"]
    assert w.spellsafe == "tax"


def test_several_words():
    with pytest.raises(BadArgumentError):
        Word("some text")
