#!/usr/bin/python
# encoding: utf-8

from workflow import Workflow
import sys


class Base(object):
    def __init__(self, args):
        self.args = unicode(args.strip(), 'utf-8')

    def execute(self):
        wf = Workflow()
        self.wf = wf
        self.log = wf.logger
        sys.exit(wf.run(self.main))

    def main(self, wf):
        pass
