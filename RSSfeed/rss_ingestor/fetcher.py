# Here we have the logic to fetcher the feeds
import feedparser

def fetch_feed_raw(url: str):
    return feedparser.parse(url)