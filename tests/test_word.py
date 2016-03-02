import unittest

from pyaspeller import Word
from pyaspeller.errors import BadArgumentError


class WordTest(unittest.TestCase):
    def test_correct_word(self):
        w = Word('test')
        self.assertTrue(w.correct)
        self.assertFalse(w.variants)
        self.assertFalse(w.spellsafe)

    def test_incorrect_word(self):
        w = Word('texx')
        self.assertFalse(w.correct)
        self.assertListEqual(w.variants, [u'tax', u'text', u'tux'])
        self.assertEqual(w.spellsafe, 'tax')

    def test_several_words(self):
        with self.assertRaises(BadArgumentError):
            Word('some text')
