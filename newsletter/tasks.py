# newsletter/tasks.py
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Subscriber
from django.template.loader import render_to_string

@shared_task
def send_newsletter_task(subject, text, html_template=None):
    emails = list(Subscriber.objects.filter(active=True).values_list('email', flat=True))
    CHUNK = 100
    for i in range(0, len(emails), CHUNK):
        chunk = emails[i:i+CHUNK]
        msg = EmailMultiAlternatives(subject, text, settings.DEFAULT_FROM_EMAIL, chunk)
        if html_template:
            html = render_to_string(html_template, {})
            msg.attach_alternative(html, 'text/html')
        msg.send()
