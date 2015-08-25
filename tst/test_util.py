#!/usr/bin/python
# encoding: utf-8

import unittest
from util import get_from_dict


class TestUtil(unittest.TestCase):

    def setUp(self):
        self.test_dict = {'x': 'b'}

    def test_get_success(self):
        result = get_from_dict(self.test_dict, 'x', 'c')
        self.assertEqual(result, 'b')

    def test_get_with_set(self):
        result = get_from_dict(self.test_dict, 'y', 'c')
        self.assertEqual(result, 'c')
        self.assertEqual({'x': 'b', 'y': 'c'}, self.test_dict)
