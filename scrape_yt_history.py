import requests
from request_object_parser import ChromeRequest
from db_api import AppDatabase

base_url = 'https://www.youtube.com'
yt_url = base_url+'/feed/history'
ref = yt_url
adb = AppDatabase();

def main():
	cr = ChromeRequest.from_file('youtube_request_headers.txt')
	rs = requests.Session()
	rs.headers.update(cr.headers)
	rs.cookies.update(cr.cookies)
	r = rs.get(cr.url)
	count = 0
	while (r.status_code == 200):
		nexturl = ''
		content = ''
		count += 1

		print "loading page ", count
		# json or html
		if ('application/json' in r.headers['content-type']):
			jdat = r.json()
			nexturl = find_next_url(jdat['load_more_widget_html'])
			content = jdat['content_html']
		else:
			nexturl = find_next_url(r.text)
			content = r.text

		if content:
			push_content(content, count)
		if nexturl != None:
			r = rs.get(base_url+nexturl, cookies=r.cookies, headers=cr.headers)
		else:
			print "find next page broke"
			with open('last error', 'w') as efile:
				efile.write(pformat(r.headers))
				efile.write(content.encode('utf8'))
			break;

	if (r.status_code != 200):
		print "Hit a bad request on page {}".format(count)
	else:
		print "Finished. Total scraped pages = {}".format(count)


def find_next_url(string):
	egg_string = 'data-uix-load-more-href="/browse_ajax?action_continuation'
	fstart = string.find(egg_string)
	nexturl = string[fstart:].split('"', 2)
	if len(nexturl) == 3:
		return nexturl[1]
	else:
		return None

def push_content(content, number):
	adb.push_page(content)


if __name__ == '__main__':
	main()