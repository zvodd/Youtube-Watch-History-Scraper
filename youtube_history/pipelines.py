# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import string

class ConvertDatesPipeline(object):
    def process_item(self, item, spider):
        if 'date' in item:
            item['date'] = self.date_parsing(item['date'])
            
        return item

    def date_parsing(self, date_string):
        # Date string is converted from MMM DD, YYYY to MM/DD/YYYY
        # TODO: Handle the parsing for upto one week prior to scraping date which is in the format of Tuesday, Friday, etc
        formatted_date = ''
       
        if "Jan" in date_string:
            formatted_date = "01"
        if "Feb" in date_string:
            formatted_date = "02"
        if "Mar" in date_string:
            formatted_date = "03"
        if "Apr" in date_string:
            formatted_date = "04"
        if "May" in date_string:
            formatted_date = "05"
        if "Jun" in date_string:
            formatted_date = "06"
        if "Jul" in date_string:
            formatted_date = "07"
        if "Aug" in date_string:
            formatted_date = "08"
        if "Sep" in date_string:
            formatted_date = "09"
        if "Oct" in date_string:
            formatted_date = "10"
        if "Nov" in date_string:
            formatted_date = "11"
        if "Dec" in date_string:
            formatted_date = "12"

        formatted_date = formatted_date + "/" + "/".join(date_string[4:].split(", "))
        return formatted_date

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