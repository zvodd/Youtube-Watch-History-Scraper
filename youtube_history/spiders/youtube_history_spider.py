import scrapy
from scrapy.http.cookies import CookieJar
from scrapy.utils.project import get_project_settings

from youtube_history.request_object_parser import ChromeRequest
from youtube_history.cookie_import import parse_cookies

from youtube_history.parse_date import find_last_date_from_string

from lxml import html

import json
import re
import sys


class YoutubeHistorySpider(scrapy.Spider):
    my_base_url = 'https://www.youtube.com'
    start_url = my_base_url+'/feed/history'

    nextlink_egg = 'data-uix-load-more-href="/browse_ajax?action_continuation'
    
    name = 'youtube_history'
    def __init__(self, *args, **kwargs):
        super(YoutubeHistorySpider, self).__init__(*args, **kwargs)
        settings = get_project_settings()
        hf = settings.get("CHROME_HEADERS_FILE")
        cj = settings.get("COOKIES_JSON")
        if hf:
            ch = ChromeRequest.from_file(hf)
            self.init_cookies = ch.cookies
        elif cj:
            with open (cj, 'r') as fh:
                cookies = parse_cookies(fh.read())
                self.init_cookies = cookies

        if not hasattr(self, "init_cookies"):
            raise ValueError("Need to specify 'CHROME_HEADERS_FILE' "+
                             "or 'COOKIES_JSON' in settings.")


    def start_requests(self):
        """
        This overide gets the first page with cookies.
        """
        yield scrapy.Request(self.start_url, cookies=self.init_cookies,
                              callback=self.parse_startpage)


    def parse_startpage(self, response):
        body = response.body_as_unicode()
        next_uri = self.sub_parse_next_link(body)
        if body.find("viewable when signed out") != -1:
            print("\n"*2," No Sign In" ,"\n")
            raise scrapy.exceptions.CloseSpider(reason='Not signed in on first page')
        for i in self.sub_parse_video_entries(body):
            yield i
        if next_uri:
            yield self.next_request(next_uri, response)


    def sub_parse_next_link(self, page_contents):
        """parse for next history page link"""
        fstart = page_contents.find(self.nextlink_egg)
        next_uri = page_contents[fstart:].split('"', 2)
        if len(next_uri) == 3:
            return next_uri[1]
        else:
            return None


    def next_request(self, next_uri, response):
        """A wrapper around 'scrapy.Request' """
        return scrapy.Request(self.my_base_url+next_uri, cookies=self.init_cookies,
                                callback=self.parse)


    def parse(self, response):
        if (b'application/json' in response.headers['Content-Type']):
            jdat = json.loads(response.body_as_unicode())
            if ('load_more_widget_html' in jdat):
                next_uri = self.sub_parse_next_link(jdat['load_more_widget_html'])
                if jdat['load_more_widget_html'].find("viewable when signed out") != -1:
                    raise scrapy.exceptions.CloseSpider(
                           reason='Not signed in on subsequent json request.')

                next_uri = self.sub_parse_next_link(jdat['load_more_widget_html'])
                if next_uri:
                    yield self.next_request(next_uri, response)

            if ('content_html' in jdat):
                content = jdat['content_html']
                for i in self.sub_parse_video_entries(content):
                    yield i
            else:
                raise scrapy.exceptions.CloseSpider(
                           reason='No history content returned on json request.')


    # TODO: Clean up this part. Add comments, Refactor variables name
    def sub_parse_video_entries(self, page_contents):
        """Method that parses the HTML bodies of the response objects"""
        etree = html.fromstring(page_contents)

        day_containers = etree.cssselect("li ol.item-section")
        for day in day_containers:
            date = None

            # Find actual container's Date
            date_element = day.cssselect("li.item-section-header h3")
            if len(date_element) == 1:
                date = date_element[0].text_content()

                date = find_last_date_from_string(date)
            
            video_container = day.cssselect('li div.yt-lockup-video')
            for video in video_container:
                video_information = {
                    "date": date,
                    "title": "",
                    "description": "",
                    "duration": "",
                    "views": "",
                    "video_url": "",
                    "channel": "",
                    "channel_url": "",
                }

                # Find Title and Video URL
                title_element = video.cssselect("h3.yt-lockup-title a.yt-uix-tile-link")
                if len(title_element) == 1:
                    video_information['title'] = title_element[0].get('title')
                    video_information['video_url'] = "https://www.youtube.com" + title_element[0].get('href')

                # Find Description
                description_element = video.cssselect('div.yt-lockup-description')
                if len(description_element) == 1:
                    video_information['description'] = description_element[0].text_content()

                # Find Duration
                time_element = video.cssselect('span.video-time')
                if len(time_element) == 1:
                    video_information['duration'] = time_element[0].text_content()
                
                # Find Views
                views_element = video.cssselect('ul.yt-lockup-meta-info li')
                if len(views_element) == 1:
                    views = views_element[0].text_content()
                    # Remove non-numeric characters from views
                    views = re.sub('[^0-9]', '', views)
                    video_information['views'] = views

                # Find Channel and Channel URL
                user_element = video.cssselect('div.yt-lockup-byline a')
                if len(user_element) == 1:
                    video_information['channel'] = user_element[0].text_content()
                    video_information['channel_url'] = "https://www.youtube.com" + user_element[0].get('href')

                yield video_information