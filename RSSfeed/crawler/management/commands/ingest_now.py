from django.core.management.base import BaseCommand
from feeds.brasil import RSS_FEED
from crawler.migrations.services import persist_ingestion_feeds

class Command(BaseCommand):
    help = "run ingestion and persist data in PostgreSQL"

    def handle(self, *args, **options):
        self.stdout.write("Saving data to database...")
        persist_ingestion_feeds(RSS_FEED)
        self.stdout.write("Data saved to the database")