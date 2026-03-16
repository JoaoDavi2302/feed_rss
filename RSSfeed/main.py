# Here we have all the logic for two things: fetching the RSS data and normalizing it, since this is a mess and nothing seems to follow a standard here.
# The core problem is normalizing all the fields in a way that makes sense without losing important data.
# This also shows the importance of discontinuing an old version after an update.

import feedparser
import time
from datetime import datetime
from feeds.brasil import RSS_FEED
from typing import Any

# This function solves the problem of the different ways feeds handle dates.
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

# This is just to monitor whether the feeds are returning entries.
# It might later become a function to sanitize entries
# if some entries are not in the format they should be.
def debug_rss_feeds(rss_list: list[str]):
     for feed_url in rss_list:
          parsed_feed = feedparser.parse(feed_url)

          if isinstance(parsed_feed.feed, dict):
               feed_title = parsed_feed.feed.get("title") or feed_url
          else:
               feed_title = feed_url

          total_entries = len(parsed_feed.entries)

          missing_link = 0
          missing_date = 0
          missing_title = 0
          valid_entries = 0

          for entry in parsed_feed.entries:
               title = entry.get("title")
               link = entry.get("link")
               date = entry.get("published_parsed") or entry.get("updated_parsed")

               if not link:
                    missing_link += 1
               if not date:
                    missing_date += 1
               if not title:
                    missing_title += 1
               if title and link and date:
                    valid_entries += 1

          discarded_entries = total_entries - valid_entries

          print(
               f"analisando o feed: {feed_url}"
               f"O feed {feed_title} trouxe {total_entries} entries, "
               f"{valid_entries} válidas e {discarded_entries} descartadas. "
               f"Faltando: {missing_link} links, {missing_date} datas, {missing_title} títulos."
          )

          if total_entries == 0:
               print(f"o feed: ${feed_url} retorna 0 entries")

# This calls the fetch function and runs it every 4 hours.
def run_scheduler(rss_list: list[str]):

    # I hate this while True. This will definitely change.
    while True:
        items = fetch_rss(rss_list)

        for item in items:
                print(item["url"])

        time.sleep(4 * 3600)

if __name__ == "__main__":
#     run_scheduler(RSS_FEED)
      debug_rss_feeds(RSS_FEED)


 