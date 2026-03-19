# main.py
from rss_ingestor.pipeline import run_ingestion_pipeline # Corrigido de 'indigestion'
from feeds.brasil import RSS_FEED

if __name__ == "__main__":
    results = run_ingestion_pipeline(RSS_FEED)
    for item in results:
        print(f"[{item['status']}] {item['dedupe_key']} - {item['title']}")