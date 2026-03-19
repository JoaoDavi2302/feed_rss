# Here we handle deduplication and control over data ingestion.
# This is important to maintain a healthy database, since we continuously ingest
# new data every four hours.

import hashlib
from datetime import datetime, timezone

def prepare_for_persistence(domain_item: dict, bacht_at: datetime) -> dict:
    persistence_item = domain_item.copy()

    url_bytes = persistence_item["url"].encode("utf-8")
    dedupe_key = hashlib.md5(url_bytes).hexdigest()

    persistence_item.update({
        "dedupe_key": dedupe_key,
        "fetched_at": bacht_at
    })

    return persistence_item