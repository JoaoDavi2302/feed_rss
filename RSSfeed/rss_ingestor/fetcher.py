# Here we have the logic to fetcher the feeds
import feedparser

def fetch_feed_raw(feed_url: str):
    return feedparser.parse(url)