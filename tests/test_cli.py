import unittest
import sys
import logging

import pyaspeller

if sys.version_info >= (3, 3):
    from unittest import mock
else:
    import mock


class CommandLineTestCase(unittest.TestCase):
    """
    Base TestCase class, sets up a CLI parser
    """

    @classmethod
    def setUpClass(cls):
        cls.args_parser = pyaspeller.create_args_parser()


class TestCLI(CommandLineTestCase):
    def test_pyaspeller_has_version(self):
        self.assertTrue(hasattr(pyaspeller, '__version__'),
                        "Module pyaspeller must have version")

    def test_correct_version(self):
        old = sys.version_info
        sys.version_info = (2, 7)
        pyaspeller.check_version()
        sys.version_info = old

    def test_min_version(self):
        old = sys.version_info
        sys.version_info = (2, 6)
        with self.assertRaises(SystemExit):
            pyaspeller.check_version()
        sys.version_info = old

    def test_default_args(self):
        args = self.args_parser.parse_args("")
        speller = pyaspeller.create_speller(args)
        self.assertTrue(speller.format == 'auto', "Bad default format")
        self.assertTrue(speller.report_type == "console",
                        "Bad default report type")
        self.assertFalse(speller.is_debug, "Can't be debuggable")
        self.assertTrue(speller.check_yo,
                        "Bad check_yo option")
        self.assertEqual(args.log_level, logging.WARNING,
                         "Bad logging level")
        self.assertEqual(args.lang, ['en', 'ru'],
                         "Bad lang")

    def test_default_ignore_args(self):
        args = self.args_parser.parse_args("")
        speller = pyaspeller.create_speller(args)

        self.assertFalse(speller.ignore_urls,
                         "Bad ignore_urls option")
        self.assertFalse(speller.ignore_tags,
                         "Bad ignore_tags option")
        self.assertFalse(speller.ignore_capitalization,
                         "Bad ignore_capitalization option")
        self.assertFalse(speller.ignore_digits,
                         "Bad ignore_digits option")
        self.assertFalse(speller.ignore_latin,
                         "Bad ignore_latin option")
        self.assertFalse(speller.ignore_roman_numerals,
                         "Bad ignore_roman_numerals option")
        self.assertFalse(speller.ignore_uppercase,
                         "Bad ignore_uppercase option")
        self.assertFalse(speller.find_repeat_words,
                         "Bad find_repeat_words option")
        self.assertFalse(speller.flag_latin,
                         "Bad flag_latin option")

    def test_debug_option(self):
        args = self.args_parser.parse_args(["--debug"])
        self.assertEqual(args.log_level, logging.DEBUG, "Bad logging level")

    def test_verbose_option(self):
        args = self.args_parser.parse_args(["--verbose"])
        self.assertEqual(args.log_level, logging.INFO,
                         "Bad logging level")

    def test_verbose_and_debug_option(self):
        args = self.args_parser.parse_args(["--verbose", "--debug"])
        self.assertEqual(args.log_level, logging.DEBUG,
                         "Bad logging level")

    def test_config_option(self):
        path = "~/.spellerrc"
        args = self.args_parser.parse_args(["--config_path", path])
        speller = pyaspeller.create_speller(args)

        self.assertIsNotNone(speller.config_path, "Bad config path")
        self.assertEqual(speller.config_path, path, "Bad config path")

    def test_empty_config_option(self):
        args = self.args_parser.parse_args(["--config_path", ''])
        speller = pyaspeller.create_speller(args)
        self.assertEqual(speller.config_path, '',
                         'Bad empty config path')

    def test_dictionary_option(self):
        path = "~/.spellerrc"
        args = self.args_parser.parse_args(["--dictionary", path])
        speller = pyaspeller.create_speller(args)

        self.assertTrue(speller.dictionary is path,
                        "Bad dictionary path")

    def test_main_checks_python_version(self):
        old_check_version = pyaspeller.check_version

        pyaspeller.check_version = mock.Mock()

        pyaspeller.main()

        self.assertTrue(pyaspeller.check_version.called,
                        "main must check version")

        pyaspeller.check_version = old_check_version
