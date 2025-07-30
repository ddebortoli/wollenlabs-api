from django.db import models
import uuid

class UrlCheck(models.Model):
    url = models.URLField()
    status_code = models.IntegerField(null=True, blank=True)
    response_time = models.FloatField(null=True, blank=True)  # in seconds
    is_reachable = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)
    batch_id = models.UUIDField(default=uuid.uuid4)

    class Meta:
        ordering = ['-checked_at']
        indexes = [
            models.Index(fields=['batch_id']),
            models.Index(fields=['checked_at']),
        ]

    def __str__(self):
        return f"{self.url} - {self.status_code or 'Pending'}"