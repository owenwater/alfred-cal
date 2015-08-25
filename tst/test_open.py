#!/usr/bin/python
# encoding: utf-8

import unittest
import mock

from open import *


class TestOpen(unittest.TestCase):

    @mock.patch('open.subprocess')
    def test_open_json_file(self, mock_sub):
        open_cal('test.json')
        mock_sub.call.assert_called_once_with(['open', 'test.json'])

    @mock.patch('open.subprocess')
    @mock.patch('workflow.Workflow')
    @mock.patch('open.Config')
    def test_open_busycal(self, mock_config, mock_wf, mock_sub):
        mock_config_instance = mock_config.return_value
        mock_config_instance.load_default.return_value = 'busycal'
        
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}

        open_cal('2000 01 01')

        mock_config_instance.load_default.assert_called_once_with('software')
        mock_sub.call.assert_called_once_with(['osascript', 'osascript/open_busycal.scpt', '2000-01-01'])

    @mock.patch('open.subprocess')
    @mock.patch('workflow.Workflow')
    @mock.patch('open.Config')
    def test_open_google_calendar(self, mock_config, mock_wf, mock_sub):
        mock_config_instance = mock_config.return_value
        mock_config_instance.load_default.return_value = 'google'
        
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}

        open_cal('2000 1 1')

        mock_config_instance.load_default.assert_called_once_with('software')
        mock_sub.call.assert_called_once_with(['osascript', 'osascript/open_google.scpt', '20000101'])
