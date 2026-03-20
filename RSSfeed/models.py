from django.db import models

class RSS_source(models.Model):
    name = models.CharField(max_length=255)
    feed_url = models.URLField(unique=True)
    is_active = models.BooleanField(default=True)

    last_fetched_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class RSS_entry(models.Model):
    source = models.ForeignKey(RSS_source, on_delete=models.CASCADE, related_name="entries")
    
    external_id = models.TextField(blank=True, null=True)
    dedupe_key = models.CharField(max_length=32, unique=True, db_index=True)

    title = models.TextField()
    url = models.URLField(max_length=1000)
    summary = models.TextField(blank=True, null=True)

    raw_content = models.JSONField()

    status = models.CharField(max_length=20, default="valid")
    published_at = models.DateField(null=True, blank=True)
    fetched_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "RSS Entries"
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.source.name}: {self.title[:50]}..."