# This is the full pipeline to fetch, normalize, and enrich data,
# preparing it for safe persistence in the database.

from datetime import datetime, timezone
from .fetcher import fetch_feed_raw
from .normalizer import normalize_entry, normalize_feed
from .persistence_model import prepare_for_persistence

def run_ingestion_pipeline(rss_urls: list[str]):
    batch_time = datetime.now(timezone.utc)
    final_entries = []

    for url in rss_urls:
        raw_data = fetch_feed_raw(url)

        source_domain = normalize_feed(raw_data, url)

        processed_entries = []
        for entry in raw_data.entries:
            normalized = normalize_entry(entry, source_domain["name"], url)
            if normalized:
                enriched_feed = prepare_for_persistence(normalized, batch_time)
                processed_entries.append(enriched_feed)

        final_entries.append({
            "source": source_domain,
            "entries": processed_entries
        })
       
    return final_entries

        