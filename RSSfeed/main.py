import feedparser
import time
from datetime import datetime
from feeds.brasil import RSS_FEED
from typing import Any

# This function solves the problem of the different ways feeds handle dates.
# I really wish they all used a single RSS version.
def parse_entry_date(entry: Any) -> datetime | None:
     published_parsed = entry.get("published_parsed") or entry.get("updated_parsed")

     if isinstance(published_parsed, time.struct_time):
          return datetime(
                published_parsed.tm_year,
                published_parsed.tm_mon,
                published_parsed.tm_mday,
                published_parsed.tm_hour,
                published_parsed.tm_min,
                published_parsed.tm_sec,
            )
     return None


# Here we have a function that standardizes the fields of the RSS sources.
# This is one of the most annoying parts of building this project, because the sources are a mess.
# Different fields and feed versions make this annoying as hell..
def normalized_entry(entry: Any, feed_title: str, feed_url:str) -> dict | None:
     url = entry.get("link")
     if not url:
          return None
     
    # The standard object that represents a news item.
     return {
          "title": entry.get("title", "No title"),
          "url": url,
          "published_date": parse_entry_date(entry),
          "feed_source": feed_title or feed_url,
          "summary": entry.get("summary") or entry.get("guid") or url,
          "raw_entry": dict(entry)
     }

# This function fetches all RSS feeds from the given list.
# It parses each feed, normalizes its entries,
# and returns a list of normalized dictionaries.
def fetch_rss(rss_list: list[str]) -> list[dict]:
        normalized_items: list[dict] = []

        for feed_url in rss_list:
            print(f"Fetching feed: {feed_url}" )
            parsed_feed = feedparser.parse(feed_url) 
            
            
            feed_meta = parsed_feed.feed
            
            # This is really ugly, but somehow it works.
            # It will probably change later.
            if isinstance(feed_meta, dict):
                 feed_title = feed_meta.get("title", feed_url)
            else:
                 feed_title = feed_url

            for entry in parsed_feed.entries:
                normalized = normalized_entry(entry, feed_title, feed_url)
                if normalized is None:
                     continue
                
                normalized_items.append(normalized)

        return normalized_items



fetch_rss(RSS_FEED)


 