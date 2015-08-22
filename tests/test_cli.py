from __future__ import print_function
import unittest
import sys

import pyaspeller


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

    def test_min_version(self):
        sys.version_info = (2, 7)
        pyaspeller.check_version()

        sys.version_info = (2, 6)
        with self.assertRaises(SystemExit):
            pyaspeller.check_version()
