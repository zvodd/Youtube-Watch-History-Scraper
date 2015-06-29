# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

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
        self.db = db_api.AppDatabase();

    def process_item(self, item, spider):
        keys = ["vid", "author_id", "title", "description", "time"]
        args = []
        for k in keys:
            args.append(item[k])

        self.db.push_video_entry(*args)
        return item