#!/usr/bin/python
# encoding: utf-8

from workflow import Workflow
from cal import Cal
from datetime import date
import sys

class Main(object):

    minus = '<'
    plus = '>'

    def __init__(self, args):
        self.args = unicode(args.strip(), 'utf-8')

    def execute(self):
        global LOG
        wf = Workflow()
        self.wf = wf
        LOG = wf.logger
        sys.exit(wf.run(self.main))

    def main(self, wf):
        cal = Cal()
        year, month = self.handle_arg()
        texts = cal.get_weeks_text(year, month)
        for text in texts:
            self.wf.add_item(text, icon = "image/blank.png")
        self.wf.send_feedback()

    def handle_arg(self):
        today = date.today()
        year = today.year
        month = today.month
        if self.args == u"":
            pass
        elif self.args.find(self.minus) != -1 or self.args.find(self.plus) != -1:
            delta = self.args.count(self.plus) - self.args.count(self.minus)
            year, month = self.change_month(year, month, delta)
        else:
            args = self.args.split()
            month = int(args[0])
            if len(args) > 1:
                year = int(args[1])
        return year, month

    def change_month(self, year, month, delta):
        month += delta
        ret_month = month % 12
        ret_year = year + month / 12 
        if ret_month == 0:
            ret_month = 12
        if month % 12 == 0:
            ret_year -= 1
        return ret_year, ret_month

if __name__=="__main__":
    main = Main("<")
    main.execute()

