##What is it?
Command line YouTube watch history scraper written in Python 2.7.
Uses pre logged in session cookies extracted from chrome.

This is just an experimental project. The database design isn't 
well thought out and there are not implemented methods for getting
information back out of the database.

You can search it manually in your favorite database browser or try using ipython.
For example:

	from db_api import *
	db = AppDatabase()
	with db._session_scope() as s:
		h_entries = s.query(HistoryEntry).filter(HistoryEntry.time > 7 * 60).limit(5)
	for he in h_entries.all():                                            
		print "{t} (http://youtube.com/watch?v={v})".format(t=he.title, v=he.vid) 

## Python library dependencies
* [requests](http://docs.python-requests.org/)
* [lxml](http://lxml.de/)
* [sqlalchemy](http://www.sqlalchemy.org/)

##How to use

###Ensure dependencies are met:

	pip install requests lxml sqlalchemy

###Getting session cookies and headers:
	
* Open chrome / chromium

* Make sure your logged into youtube.com

* Open the inspector (F12)

* Open the network tab, check the "Preserve History" box

* Visit https://youtube.com/feed/history

* Click the request for "/feed/history" in the network tab

* Copy the section "Request Headers", below the title "Request Headers"

* Paste into a new file called "youtube_request_headers.txt" in this directory

###Scraping youtube history:

	python scrape_yt_history.py

###Parsing the scraped history:

	python parse_yt_hisory.py

