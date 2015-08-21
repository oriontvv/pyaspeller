from __future__ import print_function
import unittest

import pyaspeller


class TestCLI(unittest.TestCase):

    def setUp(self):
        print("setUp")
        pyaspeller.main()

    def tearDown(self):
        print("tearDown")

    def test_pyaspeller_has_version(self):
        self.assertTrue(hasattr(pyaspeller, '__version__'),
                        "Module pyaspeller must have version")

    def test_simple(self):
        self.assertTrue(2 * 2 == 4, "simple")

    def test_simple2(self):
        self.assertFalse(2 * 2 == 5, "simple2")
