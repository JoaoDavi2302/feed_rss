# This is the full pipeline to fetch, normalize, and enrich data,
# preparing it for safe persistence in the database.

from datetime import datetime, timezone
from .fetcher import fetch_feed_raw
from .normalizer import normalize_entry
from .persistence_model import prepare_for_persistence

def run_ingestion_pipeline(rss_urls: list[str]):
    batch_time = datetime.now(timezone.utc)
    final_entries = []

    for url in rss_urls:
        raw_data = fetch_feed_raw(url)
        
        feed_info = getattr(raw_data, "feed", {})
        feed_title = feed_info.get("title", url) if isinstance(feed_info, dict) else url

        for entry in raw_data.entries:
            normalized = normalize_entry(entry, feed_title, url)
            if normalized:
                persisted = prepare_for_persistence(normalized, batch_time)
                final_entries.append(persisted)

    return final_entries

        