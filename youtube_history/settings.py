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
	'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : 500
}
ITEM_PIPELINES = {
    'youtube_history.pipelines.ConvertVideoTimePipeline': 301,
    'youtube_history.pipelines.CleanUpHistoryEntriesPipeline': 302,
    # 'youtube_history.pipelines.DbOutputPipeline': 901,
}

CHROME_HEADERS_FILE = "youtube_request_headers.txt"
# COOKIES_JSON = "youtube_cookies.json"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = ('Youtube-Watch-History-Scraper ' +
			 '(+https://github.com/AB1908/Youtube-Watch-History-Scraper)')
