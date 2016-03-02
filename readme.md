## Youtube History Scraper
A command line scraper written in Python 2.7 using scrapy and lxml.
Scrapes your YouTube History into a searchable SQLite database, so you can search for something you've previously watched.
Allowing search by video length, date published, video description, video title, etc.
Uses pre logged in session cookies extracted from chrome.

This is just an experimental project. The database design isn't 
well thought out and there are not implemented methods for getting
information back out of the database.

## Python library dependencies
* [scrapy](http://scrapy.org/)
    * [pywin32](http://sourceforge.net/projects/pywin32/) aka **win32api** Required for scrapy on windows.
* [lxml](http://lxml.de/)
* [sqlalchemy](http://www.sqlalchemy.org/)

## How to use

### Ensure dependencies are met:

	pip install scrapy lxml sqlalchemy

Windows users: You will need to install [pywin32](http://sourceforge.net/projects/pywin32/) manually; i.e. follow the link and get the installer.

You'll need a session cookie from your web broweser, so the scraper can use your account to get your history.

### Getting session cookies:

* Install the browser extension [editThisCookie](http://www.editthiscookie.com/).

* Using the same browser, goto [Youtube.com](http://www.youtube.com) and ensure you are logged in.

* Click the "editThisCookie" button, then click export. The cookies are now on you clipboard.

* Create the file "**youtube_cookies.json**" in this directory, then paste and save.
	
### Alternitive (cookies) method:

* Open chrome / chromium

* Make sure your logged into youtube.com

* Open the inspector (F12)

* Open the network tab, check the "Preserve History" box

* Visit https://youtube.com/feed/history

* Click the request for "/feed/history" in the network tab

* Copy the section "Request Headers", below the title "Request Headers"

* Paste into a new file called "youtube_request_headers.txt" in this directory

* In the **settings.py** file comment the "**COOKIES\_JSON**" line and uncomment the "**CHROME\_HEADERS\_FILE**" line.

### Run Scrapy:

	scrapy crawl yth_spider

## Profit?

You can search it manually in your favorite database browser
See [DB Browser for SQLite](http://sqlitebrowser.org/).
This way you can see the results in a table and use SQL statements to search it.

Or use ipython and sqlalchemy, this example outputs all videos > 7 minutes in length:

	from db_api import *
	db = AppDatabase()
	with db._session_scope() as s:
		h_entries = s.query(HistoryEntry).filter(HistoryEntry.time > 7 * 60).limit(5)
	for he in h_entries.all():                                            
		print "{t} (http://youtube.com/watch?v={v})".format(t=he.title, v=he.vid) 

The ````db_api```` module is just a wrapper around a sqlalchemy model and session.
````db._session_scope()```` gives you a sqlalchemy session you can run queries on, as shown above.

#### You can avoid the database output entirely
From the ***settings.py*** file just remove the line:

    'youtube_history.pipelines.DbOutputPipeline': 901,
