from __future__ import print_function
import unittest

import pyaspeller


class TestCLI(unittest.TestCase):

    def setUp(self):
        self._var = pyaspeller.test_var
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_simple(self):
        self.assertTrue(2 * self._var == 4, "simple")

    def test_simple2(self):
        self.assertFalse(2 * 2 == 5, "simple2")
