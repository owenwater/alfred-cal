#!/usr/bin/python
# encoding: utf-8

import calendar
from datetime import date
from util import get_default


class Cal(object):
    
    weekdays_name_default = u"Mo Tu We Th Fr Sa Su"
    month_name_default = u"January February March April May June July August September October November December"
    width_default = 10

    def __init__(self, settings):
        self.weekdays_name = get_default(settings, "weekdays", self.weekdays_name_default).split()
        self.month_name = get_default(settings, "month", self.month_name_default).split()
        self.width = int(get_default(settings, "width", self.width_default))
    
    def get_weeks(self, year, month, first_weekday=6):
        cal = calendar.Calendar(first_weekday)
        return list(cal.itermonthdates(year, month))

    def get_weeks_text(self, year, month, first_weekday=6):
        texts = []
        texts.append(self.month_text(year, month))
        texts.append(self.week_text(first_weekday))
        texts += self.date_text(self.get_weeks(year, month, first_weekday), first_weekday)
        return self.center(texts)

    def month_text(self, year, month):
        return self.month_name[month - 1] + "  " + str(year)
    
    def week_text(self, first_weekday):
        return ''.join([weekday.center(self.width) for weekday in self.new_weekdays_name(first_weekday)])
            
    def new_weekdays_name(self, first_weekday):
        return self.weekdays_name[first_weekday:] + self.weekdays_name[:first_weekday]

    def date_text(self, days, first_weekday):
        texts = []
        text = u" "
        current_month = days[len(days) / 2].month
        for count, day in enumerate(days):
            if day.month != current_month:
                text += " " * (self.width * 5 / 4)
            else:
                text += self.str_day(day).center(self.width)
            if count % 7 == 6:
                texts.append(text.rstrip())
                text = u" "
        return texts

    def str_day(self, day):
        if day == date.today():
            return unichr(0x2605)
        else:
            return unicode(day.day).zfill(2)

    def center(self, texts):
        texts[0] = texts[0].center(len(texts[1]))
        return texts

    def add_pre_space(self, count):
        return u" " * (count * self.width * 2 / 3)


if __name__ == "__main__":
    c = Cal()
    for line in c.get_weeks_text(2014, 11):
        print line
