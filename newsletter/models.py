# newsletter/models.py
from django.db import models
from django.utils import timezone
import uuid

class Subscriber(models.Model):
    """
    Stores subscriber emails and an unsubscribe token.
    """
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)  # inactive when unsubscribed or pending double opt-in
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    source_page = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-date_subscribed']

    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    """
    Stores messages sent through contact form.
    """
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} — {self.email}'
