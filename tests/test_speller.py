import unittest
import json
# from testfixtures import LogCapture

import pyaspeller.speller as speller


def mock_speller_responce(url):
    data = [{"code": 1, "pos": 0, "row": 0, "col": 0, "len": 4, "word": "faqe",
             "s": ["faq", "face", "fate", "fame", "fake"]},
            {"code": 1, "pos": 5, "row": 0, "col": 5,
             "len": 4, "word": "qake", "s": ["quake"]}]
    return json.dumps(data)


class NetworkOperationsUnittest(unittest.TestCase):

    def test_read_empty_url(self):
        self.assertRaises(AssertionError, speller.read_url, None)
        self.assertRaises(AssertionError, speller.read_url, '')

    # def test_logging_while_read_url(self):
    #     for url in ('http://python.org', 'fake'):
    #         with LogCapture() as l:
    #             speller.read_url(url)
    #             l.check(('root', 'DEBUG', 'reading url: ' + url),)


class BaseSpellerUnitText(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
        # speller.read_url = mock_speller_responce


class TextSpellingUnitTest(BaseSpellerUnitText):

    def test_reading_url(self):
        speller.read_url = mock_speller_responce
        self.assertIsNotNone(speller.read_url('fake'))


class UrlSpellingUnitTest(BaseSpellerUnitText):
    pass


class PathSpellingUnitTest(BaseSpellerUnitText):
    pass
