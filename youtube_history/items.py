# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YoutubeHistoryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    vid = scrapy.Field()
    channel = scrapy.Field()
    channel_url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    time = scrapy.Field()
    date = scrapy.Field()
