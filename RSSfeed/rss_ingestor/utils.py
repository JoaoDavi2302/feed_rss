from typing import Any
from datetime import datetime
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import time

# Here we process the published dates to convert them into an appropriate format.
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

# This function made the dirty work and canonicalizes all the URLs provided by the entries
def canonize_url(url: str) -> str:
    if not url:
        return " "
    # Some feeds, like folha, handle their URLs using a redirect link and the real link, separaed by a "*".
    # Here we just extract the real URL if that happens
    if "*" in url:
        url = url.split("*")[-1]

    parsed = urlparse(url)

    netloc = parsed.netloc.lower()
    
    query_params = parse_qsl(parsed.query)
    clean_params = [
        (k,v) for k, v in query_params
        if not k.startswith('utm_') and k not in ["rss", "source", "rss", "amp"]
    ]

    new_query = urlencode(clean_params)
    canonical = urlunparse((
          parsed.scheme,
          netloc,
          parsed.path.rstrip("/"),
          parsed.params,
          new_query,
          ""
     ))
    
    return canonical
