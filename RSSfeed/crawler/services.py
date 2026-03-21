from django.db import transaction
from django.utils import timezone
from crawler.models import RSS_entry, RSS_source
from rss_ingestor.pipeline import run_ingestion_pipeline

def persist_ingestion_feeds(url):
    ingestion_results = run_ingestion_pipeline(url)

    with transaction.atomic():
        for item in ingestion_results:
            source_meta = item["source"]
            entries_data = item["entries"]

            source_obj, _ = RSS_source.objects.update_or_create(
                feed_url = source_meta["feed_url"],
                defaults= {
                    "name": source_meta["name"],
                    "last_fetched_at": timezone.now()
                }
            )
        
            for entry in entries_data:
                RSS_entry.objects.update_or_create(
                    dedupe_key = entry["dedupe_key"],
                    defaults={
                        'source': source_obj,
                        'external_id': entry.get('external_id'),
                        'title': entry['title'],
                        'url': entry['url'],
                        'summary': entry['summary'],
                        'raw_content': entry['raw_content'],
                        'status': entry.get('status', 'valid'),
                        'published_at': entry['published_at'],
                        'fetched_at': entry['fetched_at'],
                    }
                )