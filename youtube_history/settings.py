# -*- coding: utf-8 -*-

# Scrapy settings for youtube_history project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'youtube_history'

SPIDER_MODULES = ['youtube_history.spiders']
NEWSPIDER_MODULE = 'youtube_history.spiders'
COOKIES_ENABLED = True
DOWNLOADER_MIDDLEWARES = {
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : 500
}
ITEM_PIPELINES = {
    'youtube_history.pipelines.ConvertVideoTimePipeline': 300,
    'youtube_history.pipelines.DbOutputPipeline': 800,
}
HEADERS_FILE = "youtube_request_headers.txt"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'youtube_history (+http://www.yourdomain.com)'
