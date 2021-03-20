# ARCHIVAL NOTICE

YouTube's front end has changed significantly, requiring JavaScript rendering of pages for web scraping. Considering this I am no longer maintaining this code base. As it was primarily just an example of a somewhat advanced Scrapy spider project.

As such, I won't be accepting pull requests or continuing development.

If you have an alternative project filling this niche, I will happy link it here:

(YouTube API V3)[https://developers.google.com/youtube/v3/docs?hl=en#Playlists}

# Youtube History Scraper

This is a tool to scrape your Youtube watching history.
After Youtube's API V3, there is no practical way to retrieve a user's complete history from the API.

This is a fork of [zvodd's scraper](https://github.com/zvodd/Youtube-Watch-History-Scraper).

**Privacy Notice: This tool download the watch history to a local file. The data is never linked to a database or other services.**

## Dependencies

Use `pip` to install the dependencies below. 
- [Python 3](https://www.python.org/downloads/)
  - [`scrapy`](http://scrapy.org/)
  - [`lxml`](http://lxml.de/)

## Usage

### Prerequisites

Scrapy requires a cookie to export a user's history. A template has already been provided in `youtube_request_headers.txt`. The only field that **needs to be filled in by the user** is **`cookie`**. This can be obtained by doing the following:

1. Open a web browser.
2. Open the Inspect Console by pressing `Ctrl+Shift+I` (may vary by browser).
3. Open the `Network` tab and enable `Preserve Logs` or a similar option.
4. Assuming one is signed in to their account, go to the [YouTube history page](https://youtube.com/feed/history).
5. Find the corresponding log entry for the `history` page in the `Network` tab which should be a **`GET`** request.
6. From the `Raw Header` data (may need to toggle this on), copy the `Cookie` field from the **Request Headers** section into `youtube_request_headers.txt` already present in the repository.

### Running the scraper

To run the scraper and export the data as a CSV, open a terminal/shell and run the following:

```
	-> scrapy crawl youtube_history -o output/history.csv -L ERROR
```

The `-L` argument will output errors.

## Output Format

The CSV is output in the following format:

| Date | Title | Description | Duration | Views | Video URL | Channel Name | Channel URL |
|--|--|--|--|--|--|--|


## Contribution

Any contribution is welcome, whether it be feedback, an issue, a pull request.

## License

I'd be happy to license this code under an MIT 2.0 License but the original repository doesn't have a license and I thus have no right. They have sole ownership of the code and thus reserve the right for this to be taken down. This will be modified to include a license in the future if possible.
