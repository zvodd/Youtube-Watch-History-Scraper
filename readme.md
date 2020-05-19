# Youtube History Scraper

This tool can be used to scrape YouTube history after their history API changed to only allow fetching the last two weeks' worth of data. There might exist a project to use that API periodically to log history from a certain time onwards
but [zvodd's scraper](https://github.com/zvodd/Youtube-Watch-History-Scraper) exports all history. It was originally in Python 2.7 and had no date parser and were added in this fork. This project is purely experimental and there is no error handling.

**Privacy Notice: This tool only exports data locally and does not send your information elsewhere.**

## Dependencies

Use `pip` to install the dependencies below. Also note that `pywin32`'s `pip` support is experimental. See [their repo](https://github.com/mhammond/pywin32) for details.

### Required

- [Python 3](https://www.python.org/downloads/)
  - [`scrapy`](http://scrapy.org/)
  - [`lxml`](http://lxml.de/)

### Optional

- Python 3  
  - [`sqlalchemy`](http://www.sqlalchemy.org/) (optional)
  - [`pywin32`](https://github.com/mhammond/pywin32) (**for Windows users only**)

## Usage

### Prerequisites

Scrapy requires a cookie to export a user's history. A template has already been provided in `youtube_request_headers.txt`. The only field that **needs to be filled in by the user** is **`cookie`**. This can be obtained by doing the following:

1. Open a web browser.
2. Open the Inspect Console by pressing `Ctrl+Shift+I` (may vary by browser).
3. Open the `Network` tab and enable `Preserve Logs` or a similar option.
4. Assuming one is signed in to their account, go to the [YouTube history page](https://youtube.com/feed/history).
5. Find the corresponding log entry for the history page in the `Network` tab which should be a **`GET`** request.
6. From the `Raw Header` data (may need to toggle this on), copy the `Cookie` field from the **Request Headers** section into `youtube_request_headers.txt` already present in the repository. It's a pretty big string unfortunately.

### Running scrapy

To run the scraper and export the data as a CSV, open a terminal/shell of your choice and run the following:

```
	shell> scrapy crawl yth_spider -o history.csv -L ERROR
```

**Note: This may take a while.**

The `-L` argument will output errors. Feel free to open issues if you encounter them. Once it's done, import the CSV into a tool of your choice.

## Output Format

The CSV is output in the following format:

| Channel Name | Channel URL | Date | Description | Time (in seconds) | Title | Video URL |
|--|--|--|--|--|--|--|

## Known Issues

The data from upto a week before is displayed as days of the week, i.e. Sunday, Monday, etc. Any way to parse this would be appreciated. For now, just change them manually.

## Contribution

Any contribution is welcome, whether it be feedback, an issue, a pull request.

## License

I'd be happy to license this code under an MIT 2.0 License but the original repository doesn't have a license and I thus have no right. They have sole ownership of the code and thus reserve the right for this to be taken down. This will be modified to include a license in the future if possible.