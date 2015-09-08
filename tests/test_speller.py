import unittest
import json
# from testfixtures import LogCapture

# import pyaspeller
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

    # def test_call_main(self):
    #     pyaspeller.main()

    def test_reading_url(self):
        speller.read_url = mock_speller_responce
        self.assertIsNotNone(speller.read_url('fake'))

    def test_bad_single_lang_property(self):
        self.assertRaises(AssertionError, speller.YandexSpeller, lang='qwe')

    def test_correct_lang_property(self):
        sp = speller.YandexSpeller(lang=('ru', 'en'))
        self.assertEqual(sp.lang, ['ru', 'en'], 'Bad language')

    def test_correct_single_lang_property(self):
        sp = speller.YandexSpeller(lang=('en',))
        self.assertEqual(sp.lang, ['en'], 'Bad language')

    def test_correct_single_lang_str_property(self):
        sp = speller.YandexSpeller(lang='uk')
        self.assertEqual(sp.lang, ['uk'], 'Bad language')

    def test_check_lang_property(self):
        sp = speller.YandexSpeller()
        sp.lang = 'en'
        self.assertEqual(sp.lang, ['en'], 'Bad language')

    def test_check_ignore_uppercase_option(self):
        sp = speller.YandexSpeller()

        self.assertFalse(sp.api_options & 1, 'Bad ignore_uppercase option')
        self.assertFalse(sp.api_options & 2, 'Bad ignore_digits option')
        self.assertFalse(sp.api_options & 4, 'Bad ignore_urls option')
        self.assertTrue(sp.api_options & 8, 'Bad find_repeat_words option')
        self.assertFalse(sp.api_options & 16, 'Bad ignore_latin option')
        self.assertTrue(sp.api_options & 128, 'Bad flag_latin option')
        self.assertFalse(sp.api_options & 512, 'Bad ignore_capitalization '
                                               'option')

    def test_check_ignore_uppercase_option_inverse(self):
        sp = speller.YandexSpeller(ignore_uppercase=True,
                                   ignore_digits=True,
                                   ignore_urls=True,
                                   find_repeat_words=False,
                                   ignore_latin=True,
                                   flag_latin=False,
                                   ignore_capitalization=True)

        self.assertTrue(sp.api_options & 1, 'Bad ignore_uppercase option')
        self.assertTrue(sp.api_options & 2, 'Bad ignore_digits option')
        self.assertTrue(sp.api_options & 4, 'Bad ignore_urls option')
        self.assertFalse(sp.api_options & 8, 'Bad find_repeat_words option')
        self.assertTrue(sp.api_options & 16, 'Bad ignore_latin option')
        self.assertFalse(sp.api_options & 128, 'Bad flag_latin option')
        self.assertTrue(sp.api_options & 512, 'Bad ignore_capitalization '
                                              'option')


class UrlSpellingUnitTest(BaseSpellerUnitText):
    pass


class PathSpellingUnitTest(BaseSpellerUnitText):
    pass
