import pytest

from pyaspeller import Word
from pyaspeller.errors import BadArgumentError


def test_correct_word():
    w = Word('test')
    assert w.correct
    assert not w.variants
    assert not w.spellsafe


def test_incorrect_word():
    w = Word('taxx')
    assert not w.correct
    assert w.variants == [u'tax', u'texx', u'tixx']
    assert w.spellsafe == 'tax'


def test_several_words():
    with pytest.raises(BadArgumentError):
        Word('some text')
