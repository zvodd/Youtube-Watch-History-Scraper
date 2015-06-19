import scrapy
from scrapy.utils.project import get_project_settings
# from ipdb import set_trace as debug
from youtube_history.items import YoutubeHistoryItem
from youtube_history.request_object_parser import ChromeRequest
from scrapy.http.cookies import CookieJar
from lxml import html
import json

class YoutubeHistorySpider(scrapy.Spider):
    my_base_url = 'https://www.youtube.com'
    start_url = my_base_url+'/feed/history'

    nextlink_egg = 'data-uix-load-more-href="/browse_ajax?action_continuation'
    
    name = 'yth_spider'
    def __init__(self, *args, **kwargs):
        super(YoutubeHistorySpider, self).__init__(*args, **kwargs)
        settings = get_project_settings()
        hf = settings.get("HEADERS_FILE")
        if hf:
            ch = ChromeRequest.from_file(hf)
            self.init_headers = ch.headers
            self.init_cookies = ch.cookies
            self.init_headers["User-Agent"] = ch.user_agent

        if not hasattr(self, "init_headers"):
            raise ValueError("Need to specify 'HEADERS_FILE' in settings.")


    def start_requests(self):
        """ Overridden, starts the first page, injects headers(unnecessarily) and cookies."""
        yield scrapy.Request(self.start_url, cookies=self.init_cookies,
                             headers=self.init_headers, callback=self.parse_startpage)


    def parse_startpage(self, response):
        next_uri = self.sub_parse_next_link(response.body)
        if response.body.find("viewable when signed out") != -1:
            print "\n"*2," No Sign In" ,"\n"*2,
            raise scrapy.exceptions.CloseSpider(reason='Not signed in on first page')
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
        return scrapy.Request(self.my_base_url+next_uri, cookies=self.init_cookies, callback=self.parse)


    def parse(self, response):
        if ('application/json' in response.headers['content-type']):
            jdat = json.loads(response.body)
            if ('load_more_widget_html' in jdat):
                next_uri = self.sub_parse_next_link(jdat['load_more_widget_html'])
                if jdat['load_more_widget_html'].find("viewable when signed out") != -1:
                    raise scrapy.exceptions.CloseSpider(
                           reason='Not signed in on subsequent page')

                next_uri = self.sub_parse_next_link(jdat['load_more_widget_html'])
                if next_uri:
                    yield self.next_request(next_uri, response)

            if ('content_html' in jdat):
                content = jdat['content_html']
                for i in self.sub_parse_video_entries(content):
                    yield i


    def sub_parse_video_entries(self, page_contents):
        """Does the actual data extraction"""
        etree = html.fromstring(page_contents)
        video_fragments = etree.cssselect('li div.yt-lockup-video')
        for entry in video_fragments:
            hitem = YoutubeHistoryItem()
            title_element = entry.cssselect("h3.yt-lockup-title a.yt-uix-tile-link")

            if len(title_element) == 1:
                title_element = title_element[0]
                hitem['title'] = title_element.get('title')
                hitem['vid'] = title_element.get('href').replace('/watch?v=', '')
            user_el = entry.cssselect('div.yt-lockup-byline a')
            if len(user_el) == 1:
                user_el = user_el[0]
                hitem['author_id'] = user_el.get('href').replace('/user/', '')

            descp_el = entry.cssselect('div.yt-lockup-description')
            if len(descp_el) == 1:
                descp_el = descp_el[0]
                hitem['description'] = descp_el.text_content()
            else:
                hitem['description'] = None

            vtime_el = entry.cssselect('span.video-time')
            if len(vtime_el) == 1:
                hitem['time'] = vtime_el[0].text
            yield hitem