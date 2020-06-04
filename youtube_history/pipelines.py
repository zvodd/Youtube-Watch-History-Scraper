# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import string

class ConvertDatesPipeline(object):
    def process_item(self, item, spider):
        item['date'] = self.date_parsing(item['date'])
        return item

    def date_parsing(self, datestring):
        # Date string is converted from MMM DD, YYYY to MM/DD/YYYY
        # TODO: Handle the parsing for upto one week prior to scraping date which is in the format of Tuesday, Friday, etc
        if "Jan" in datestring:
            formatteddate = "01"
        if "Feb" in datestring:
            formatteddate = "02"
        if "Mar" in datestring:
            formatteddate = "03"
        if "Apr" in datestring:
            formatteddate = "04"
        if "May" in datestring:
            formatteddate = "05"
        if "Jun" in datestring:
            formatteddate = "06"
        if "Jul" in datestring:
            formatteddate = "07"
        if "Aug" in datestring:
            formatteddate = "08"
        if "Sep" in datestring:
            formatteddate = "09"
        if "Oct" in datestring:
            formatteddate = "10"
        if "Nov" in datestring:
            formatteddate = "11"
        if "Dec" in datestring:
            formatteddate = "12"
        formatteddate = formatteddate + "/" + "/".join(datestring[4:].split(", "))
        return formatteddate

class CleanUpHistoryEntriesPipeline(object):
    def proccess_items(self, item, spider):
        item['vid'] = item['vid'].replace('/watch?v=', '')
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