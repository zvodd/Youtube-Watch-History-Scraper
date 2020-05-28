# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import string
from datetime import date, datetime, timedelta


class ConvertDatesPipeline(object):
    def process_item(self, item, spider):
        item['date'] = self.date_parsing(item['date'])
        return item

    def date_parsing(self, datestring):
        today = date.today()
        weekdays = {
            (today - timedelta(i)).strftime("%A"): today - timedelta(i)
            for i in range(2, 7)
        }
        weekdays["Today"] = today
        weekdays["Yesterday"] = today - timedelta(1)

        re1 = re.compile(
            r"([JFMASOND][aepuco][nbrylgptvc]) (\d{1,2})(, 2\d{3})*")
        if datestring in weekdays.keys():
            return weekdays[datestring]
        else:
            m = re1.match(datestring)
            if m.groups()[2] is None:
                datestring += f", {today.year}"
            return datetime.strptime(datestring, "%b %d, %Y").date()


class CleanUpHistoryEntriesPipeline(object):
    def proccess_items(self, item, spider):
        item['vid'] = item['vid'].replace('/watch?v=', '')
        # item['author_id'] = item['author_id'].replace('/user/', '')
        # item['author_id'] = item['author_id'].replace('/channel/', '')
        return item


class ConvertVideoTimePipeline(object):
    def process_item(self, item, spider):
        item['time'] = self.convert_time(item['time'])
        return item

    def convert_time(self, tstring):
        seconds, minutes, hours = None, None, None
        total_seconds = 0
        t_components = tstring.strip().split(':')
        for i, comp in enumerate(reversed(t_components)):
            if i == 0:
                seconds = int(comp)
                total_seconds = seconds
            if i == 1:
                minutes = int(comp)
                total_seconds += minutes * 60
            if i == 2:
                hours = int(comp)
                total_seconds += hours * 3600
        return total_seconds


class DbOutputPipeline(object):
    def __init__(self, *args, **kwargs):
        super(DbOutputPipeline, *args, **kwargs)
        from youtube_history import db_api
        self.db = db_api.AppDatabase()

    def process_item(self, item, spider):
        keys = ["vid", "channel", "channel_url",
                "title", "description", "time", "date"]
        args = []
        for k in keys:
            args.append(item[k])

        self.db.push_video_entry(*args)
        return item
