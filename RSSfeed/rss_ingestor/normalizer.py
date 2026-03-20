# This normalizes the entries.
# Everything that comes from the feed is a mess, and nothing follows a standard.
# So, we have to standardize it into an object to persist in the database.

from typing import Any
from .utils import canonize_url, parse_entry_date

def normalize_entry(entry: Any, feed_title: str, feed_url: str) -> dict | None:
    title = entry.get("title", "").strip()
    raw_url = entry.get("link")

    clean_url = canonize_url(raw_url)
    published_at = parse_entry_date(entry)
    external_id = entry.get("id") or entry.get("guid")

    if not clean_url or not title or title.lower() == "no title":
        return None
    
    status = "valid" if published_at else "partial"

    return {
        "external_id": external_id,
        "title": title,
        "url": clean_url,
        "published_at": published_at,
        "feed_url": feed_url,
        "status": status,
        "summary": entry.get("summary") or "",
        "raw_conent": dict(entry)
    }

def normalize_feed(raw_feed_data: Any, feed_url: str) -> dict:
    feed_meta = getattr(raw_feed_data, "feed", {})

    feed_title = feed_meta.get("title", feed_url).strip()

    return {
        "name":feed_title,
        "feed_url": feed_url,
        "description": feed_meta.get("description", ""),
    } 