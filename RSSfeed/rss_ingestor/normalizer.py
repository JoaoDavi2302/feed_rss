from typing import Any, Optional, Dict
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