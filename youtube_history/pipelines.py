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
        if 'time' in item:
            item['time'] = self.convert_time_to_seconds(item['time'])
        return item

    def convert_time_to_seconds(self, time):
        total_seconds = 0
        splitted_time = time.strip().split(':')

        for index, time_digit in enumerate(reversed(splitted_time)):
            if index == 0:
                seconds = int(time_digit)
                total_seconds = seconds
            if index == 1:
                minutes = int(time_digit)
                total_seconds += minutes * 60
            if index == 2:
                hours = int(time_digit)
                total_seconds += hours * 3600

        return total_seconds