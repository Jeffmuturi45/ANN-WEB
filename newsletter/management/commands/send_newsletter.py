# newsletter/management/commands/send_newsletter.py
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from newsletter.models import Subscriber
from django.template.loader import render_to_string

CHUNK = 100

class Command(BaseCommand):
    help = 'Send newsletter to all active subscribers. Usage: python manage.py send_newsletter "Subject" "plain text" --html=template.html'

    def add_arguments(self, parser):
        parser.add_argument('subject')
        parser.add_argument('text')
        parser.add_argument('--html', help='Template path within templates/ (optional)')

    def handle(self, *args, **options):
        subject = options['subject']
        text_body = options['text']
        html_template = options.get('html')
        emails = list(Subscriber.objects.filter(active=True).values_list('email', flat=True))
        total = len(emails)
        self.stdout.write(f'Found {total} active subscribers.')
        for i in range(0, total, CHUNK):
            chunk = emails[i:i+CHUNK]
            try:
                msg = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL, chunk)
                if html_template:
                    html_content = render_to_string(html_template, {})
                    msg.attach_alternative(html_content, 'text/html')
                msg.send()
                self.stdout.write(f'Sent chunk {i//CHUNK + 1} ({len(chunk)} recipients)')
            except Exception as e:
                self.stderr.write(f'Error sending chunk {i//CHUNK + 1}: {e}')
