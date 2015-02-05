#!/usr/bin/python
# encoding: utf-8

from workflow import Workflow
from cal import Cal
from datetime import date
import sys


class Main(object):

    minus_default = u'<'
    plus_default = u'>'
    weekdays_name_default = u"Mo Tu We Th Fr Sa Su"
    month_name_default = u"January February March April May June July August September October November December"
    width_default = 10
    highlight_today_default = True



    config_option = u"config"
    config_desc = u"Open config file"

    def __init__(self, args):
        self.args = unicode(args.strip(), 'utf-8')

    def execute(self):
        global LOG
        wf = Workflow()
        self.wf = wf
        LOG = wf.logger
        
        self.minus = wf.settings.setdefault('minus', self.minus_default)
        self.plus = wf.settings.setdefault('plus', self.plus_default)
        wf.settings.setdefault('weekdays', self.weekdays_name_default).split()
        wf.settings.setdefault("month", self.month_name_default).split()
        wf.settings.setdefault("width", self.width_default)
        wf.settings.setdefault("highlight_today", self.highlight_today_default)

        sys.exit(wf.run(self.main))

    def main(self, wf):
        cal = Cal(wf.settings, wf.alfred_env['theme'], wf.alfred_env['preferences'])
        year, month = self.handle_arg()
        if year == -1 and month == -1:
            return
        texts = cal.get_weeks_text(year, month)
        for index, text in enumerate(texts):
            if index == 0:
                self.wf.add_item(text)
            elif index < 2:
                self.wf.add_item(text, icon="image/blank.png")
            else:
                arg = "%d %d %s" % (year, month, text.strip().split()[0])
                self.wf.add_item(text, icon="image/biank.png", arg=arg, valid=True)
        self.wf.send_feedback()

    def handle_arg(self):

        if self.config_option.startswith(self.args) and len(self.args) > 0:
            self.wf.add_item(self.config_desc, valid=True, arg=self.wf.settings_path, autocomplete=self.config_option)
            self.wf.send_feedback()
            return -1, -1

        argv = self.args.split()
        today = date.today()

        month = self.to_month(self.get_item(argv, 0), today.month)
        year = self.to_year(self.get_item(argv, 1), today.year)
        
        if month <= 0 or month > 12:
            raise ValueError("month must be in 1..12")
        
        delta_str = self.get_item(argv, -1, "")
        delta = delta_str.count(self.plus) - delta_str.count(self.minus)

        year, month = self.change_month(year, month, delta)

        return year, month

    def get_item(self, arr, index, default_value=None):
        try:
            return arr[index]
        except IndexError:
            return default_value

    def to_month(self, month, default_month):
        try:
            return int(month)
        except TypeError:
            return default_month
        except:
            month = month.lower()
            for i, cal_month in enumerate(self.wf.settings['month'].split()):
                if cal_month.lower().startswith(month):
                    return i + 1
            raise Exception('Invalid month argument.')


    def to_year(self, year, default_year):
        try:
            return int(year)
        except:
            return default_year

    def change_month(self, year, month, delta):
        month += delta
        ret_month = month % 12
        ret_year = year + month / 12
        if ret_month == 0:
            ret_month = 12
        if month % 12 == 0:
            ret_year -= 1
        return ret_year, ret_month


if __name__ == "__main__":
    main = Main(" ".join(sys.argv[1:]))
    main.execute()
