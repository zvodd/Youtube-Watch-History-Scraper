from db_api import AppDatabase
from lxml import html
from pprint import pprint

adb = AppDatabase();


def main():
	total = adb.get_total_raw_pages()
	print "total page: ", total
	for pageoffset in range(0, total):
		pagecontent = adb.get_raw_page(pageoffset)
		parse_page(pagecontent)

def parse_page(page_contents):

	etree = html.fromstring(page_contents)
	video_fragments = etree.cssselect('li div.yt-lockup-video')
	for entry in reversed(video_fragments):
		vid, author_id, title, description, time = None, None, None, "", None
		title_element = entry.cssselect("h3.yt-lockup-title a.yt-uix-tile-link")
		if len(title_element) == 1:
			title_element = title_element[0]
			title = title_element.get('title')
			vid = title_element.get('href').replace('/watch?v=', '')
		user_el = entry.cssselect('div.yt-lockup-byline a')
		if len(user_el) == 1:
			user_el = user_el[0]
			author_id = user_el.get('href').replace('/user/', '')

		descp_el = entry.cssselect('div.yt-lockup-description')
		if len(descp_el) == 1:
			descp_el = descp_el[0]
			description = descp_el.text_content()

		vtime_el = entry.cssselect('span.video-time')
		if len(vtime_el) == 1:
			time = convert_time(vtime_el[0].text)
			

		push_vid_entry(vid, author_id, title, description, time)


def convert_time(tstring):
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


def push_vid_entry(vid, author_id, title, description, time):
	args = [vid, author_id, title, description, time]
	pprint (args)
	# assert(all(args))
	adb.push_video_entry(*args)

if __name__ == '__main__':
	main()