#!/usr/bin/python
# encoding: utf-8

from workflow import Workflow
import sys


DEFAULT_SETTINGS = {
  "first_day": 6, 
  "highlight_today": True, 
  "minus": "<", 
  "month": "January February March April May June July August September October November December", 
  "plus": ">", 
  "software": "calendar", 
  "weekdays": "Mo Tu We Th Fr Sa Su", 
  "width": 10
}

class Base(object):
    def __init__(self, args):
        self.args = unicode(args.strip(), 'utf-8')

    def execute(self):
        wf = Workflow(default_settings = DEFAULT_SETTINGS)
        self.wf = wf
        self.log = wf.logger
        sys.exit(wf.run(self.main))

    def main(self, wf):
        pass

