#!/usr/bin/python
# encoding: utf-8

import unittest
import mock
import os

from config import Config

CONFIG = 'config.json'
SETTINGS_PATH = 'settings_path'

config_json = [
    {
        "name": "i1_n",
        "type": "int",
        "keyword": "i1_k",
        "description": "i1_d",
        "default": 2,
        "min": 1,
        "max": 3
    },
    {
        "name": "s1_n",
        "type": "str",
        "keyword": "s1_k",
        "description": "s1_d",
        "default": "s1"
    },
    {
        "name": "s2_n",
        "type": "str",
        "keyword": "s2_k",
        "description": "s2_d",
        "default": "s2"
    },
    {
        "name": "i2_n",
        "type": "int",
        "keyword": "i2_k",
        "description": "i2_d",
        "list": [
            ["oa1", 0],
            ["oa2", 1],
            ["o3", 2]
        ],
        "default": 1
    },
    {
        "description": "ocf",
        "keyword": "config",
        "action": "open"
    }
]


class TestConfig(unittest.TestCase):

    def setUp(self):
        import json
        with open(CONFIG, 'w') as fp:
            json.dump(config_json, fp)

    def tearDown(self):
        os.unlink(CONFIG)

    @mock.patch('config.json')
    def test_load_default(self, mock_json):
        mock_json.load.return_value = [{'name': 'x', 'default': 'a'}]

        result = Config('').load_default('x')

        self.assertEqual(result, 'a')
        self.assertEqual(mock_json.load.call_count, 1)

    @mock.patch('config.json')
    def test_can_not_load_default(self, mock_json):
        mock_json.load.return_value = [{'name': 'x', 'default': 'a'}]

        result = Config('').load_default('y')

        self.assertEqual(result, None)
        self.assertEqual(mock_json.load.call_count, 1)

    @mock.patch('config.json')
    def test_multiple_load_default(self, mock_json):
        mock_json.load.return_value = [{'name': 'x', 'default': 'a'}]
        config = Config('')

        result1 = config.load_default('x')
        result2 = config.load_default('y')

        self.assertEqual(result1, 'a')
        self.assertEqual(result2, None)
        self.assertEqual(mock_json.load.call_count, 1)

    @mock.patch('workflow.Workflow')
    def test_set_int_value(self, mock_wf):
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {'a': 1, 'b': 'x'}

        config = Config('a 3')
        config.set_value()
        self.assertEqual(mock_wf_instance.settings, {'a': 3, 'b': 'x'})

    @mock.patch('workflow.Workflow')
    def test_set_str_value(self, mock_wf):
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {'a': 1, 'b': 'x'}

        config = Config('b yy')
        config.set_value()
        self.assertEqual(mock_wf_instance.settings, {'a': 1, 'b': 'yy'})

    @mock.patch('subprocess.call')
    @mock.patch('workflow.Workflow')
    def test_set_open_config_file(self, mock_wf, mock_sub_call):
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings_path = SETTINGS_PATH

        config = Config('open_config_file')
        config.set_value()

        mock_sub_call.assert_called_once_with(['open', SETTINGS_PATH])
        self.assertEquals(mock_sub_call.call_count, 1)

    @mock.patch('workflow.Workflow')
    def test_show_config_list(self, mock_wf):
        config = Config('')
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}
        config.wf = mock_wf_instance

        config.main(mock_wf_instance)

        calls = [
            mock.call(u'i1_d', subtitle=u'Current: 2', autocomplete=u'i1_k '),
            mock.call(u's1_d', subtitle=u'Current: s1', autocomplete=u's1_k '),
            mock.call(u's2_d', subtitle=u'Current: s2', autocomplete=u's2_k '),
            mock.call(u'i2_d', subtitle=u'Current: oa2', autocomplete=u'i2_k '),
            mock.call(u'ocf', subtitle='', autocomplete=u'config '),
        ]
        mock_wf_instance.add_item.assert_has_calls(calls)
        mock_wf_instance.send_feedback.assert_called_once_with()
    
    @mock.patch('workflow.Workflow')
    def test_show_config_list_with_filter(self, mock_wf):
        config = Config('i')
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}
        config.wf = mock_wf_instance

        config.main(mock_wf_instance)

        calls = [
            mock.call(u'i1_d', subtitle=u'Current: 2', autocomplete=u'i1_k '),
            mock.call(u'i2_d', subtitle=u'Current: oa2', autocomplete=u'i2_k '),
        ]
        mock_wf_instance.add_item.assert_has_calls(calls)
        mock_wf_instance.send_feedback.assert_called_once_with()

    @mock.patch('workflow.Workflow')
    def test_show_config_list_with_action(self, mock_wf):
        config = Config('config')
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}
        config.wf = mock_wf_instance

        config.main(mock_wf_instance)

        mock_wf_instance.add_item.assert_called_once_with(u'ocf', arg=u'open_config_file', valid=True)
        mock_wf_instance.send_feedback.assert_called_once_with()

    @mock.patch('workflow.Workflow')
    def test_show_one_item_without_value(self, mock_wf):
        config = Config('i1_k')
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}
        config.wf = mock_wf_instance

        config.main(mock_wf_instance)

        mock_wf_instance.add_item.assert_called_once_with(u'i1_d', subtitle=u'Current: 2', autocomplete=u'i1_k ')
        mock_wf_instance.send_feedback.assert_called_once_with()

    @mock.patch('workflow.Workflow')
    def test_show_str_item(self, mock_wf):
        config = Config('s1_k v')
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}
        config.wf = mock_wf_instance

        config.main(mock_wf_instance)

        mock_wf_instance.add_item.assert_called_once_with(u's1_d', arg=u's1_n v',
                                                          subtitle=u'Current: s1, set to: v', valid=True)
        mock_wf_instance.send_feedback.assert_called_once_with()

    @mock.patch('workflow.Workflow')
    def test_show_int_item(self, mock_wf):
        config = Config('i1_k 1')
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}
        config.wf = mock_wf_instance

        config.main(mock_wf_instance)

        mock_wf_instance.add_item.assert_called_once_with(u'i1_d', arg=u'i1_n 1',
                                                          subtitle=u'Current: 2, set to: 1', valid=True)
        mock_wf_instance.send_feedback.assert_called_once_with()

    @mock.patch('workflow.Workflow')
    def test_invalid_int_value(self, mock_wf):
        config = Config('i1_k k')
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}
        config.wf = mock_wf_instance

        config.main(mock_wf_instance)

        mock_wf_instance.add_item.assert_called_once_with('Please enter an integer')
        mock_wf_instance.send_feedback.assert_called_once_with()

    @mock.patch('workflow.Workflow')
    def test_int_too_small(self, mock_wf):
        config = Config('i1_k 0')
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}
        config.wf = mock_wf_instance

        config.main(mock_wf_instance)

        mock_wf_instance.add_item.assert_called_once_with('Value must be between 1 and 3')
        mock_wf_instance.send_feedback.assert_called_once_with()

    @mock.patch('workflow.Workflow')
    def test_int_too_large(self, mock_wf):
        config = Config('i1_k 10')
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}
        config.wf = mock_wf_instance

        config.main(mock_wf_instance)

        mock_wf_instance.add_item.assert_called_once_with('Value must be between 1 and 3')
        mock_wf_instance.send_feedback.assert_called_once_with()

    @mock.patch('workflow.Workflow')
    def test_list_item(self, mock_wf):
        config = Config('i2_k')
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}
        config.wf = mock_wf_instance

        config.main(mock_wf_instance)

        calls = [
            mock.call(u'oa1', arg=u'i2_n 0', autocomplete=u'i2_k oa1', valid=True),
            mock.call(u'oa2 (selected)', arg=u'i2_n 1', autocomplete=u'i2_k oa2', valid=True),
            mock.call(u'o3', arg=u'i2_n 2', autocomplete=u'i2_k o3', valid=True)
        ]
        mock_wf_instance.add_item.assert_has_calls(calls)
        mock_wf_instance.send_feedback.assert_called_once_with()

    @mock.patch('workflow.Workflow')
    def test_list_item_with_filter(self, mock_wf):
        config = Config('i2_k oa')
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}
        config.wf = mock_wf_instance

        config.main(mock_wf_instance)

        calls = [
            mock.call(u'oa1', arg=u'i2_n 0', autocomplete=u'i2_k oa1', valid=True),
            mock.call(u'oa2 (selected)', arg=u'i2_n 1', autocomplete=u'i2_k oa2', valid=True),
        ]
        mock_wf_instance.add_item.assert_has_calls(calls)
        mock_wf_instance.send_feedback.assert_called_once_with()

    @mock.patch('workflow.Workflow')
    def test_list_item_with_filter_to_one_item(self, mock_wf):
        config = Config('i2_k oa1')
        mock_wf_instance = mock_wf.return_value
        mock_wf_instance.settings = {}
        config.wf = mock_wf_instance

        config.main(mock_wf_instance)

        calls = [
            mock.call(u'oa1', arg=u'i2_n 0', autocomplete=u'i2_k oa1', valid=True),
        ]
        mock_wf_instance.add_item.assert_has_calls(calls)
        mock_wf_instance.send_feedback.assert_called_once_with()
