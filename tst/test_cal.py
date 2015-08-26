#!/usr/bin/python
# encoding: utf-8

import unittest

from cal import Cal
from util import DEFAULT_SETTINGS


class TestCal(unittest.TestCase):

    def setUp(self):
        self.settings = DEFAULT_SETTINGS
        self.cal = Cal(DEFAULT_SETTINGS, 'key', 'path')
