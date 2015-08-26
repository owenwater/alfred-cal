#!/usr/bin/python
# encoding: utf-8

import unittest
import mock

from base import Base


class TestBase(unittest.TestCase):

    def test_arg_strip(self):
        base = Base('  mock_arg  ')
        self.assertEqual(base.args, u'mock_arg')

    def test_arg_unicode(self):
        base = Base('测试参数')
        self.assertEqual(base.args, u'\u6d4b\u8bd5\u53c2\u6570')

    @mock.patch('base.sys')
    @mock.patch('base.Workflow')
    def test_execute(self, mock_wf, mock_sys):
        base = Base('mock_arg')
        mock_wf_instance = mock_wf.return_value
        
        base.execute()

        self.assertEqual(base.wf, mock_wf_instance)
        self.assertEqual(base.log, mock_wf_instance.logger)
        mock_wf_instance.run.assert_called_once_with(base.main)
        mock_sys.exit.has_called()
