# Here is the function that fetches the XML from the RSS source.
# It runs every 4 hours. This interval is arbitrary and can be changed.
# Keep in mind that if you add many RSS sources, processing all links may lead to performance issues.
import feedparser
import time
from datetime import datetime
from feeds.brasil import RSS_FEED

# this while true is ugly and will be changed.

while True:
    for feed in RSS_FEED:
        print(f"Fetching feed: {feed}" )
        f = feedparser.parse(feed) 

        for entry in f.entries:
            title = entry.get("title")
            url = entry.get("link")
            published_parsed = entry.get("published_parsed")
                
            print(title)

            if not url:
                continue



    time.sleep(10)


 