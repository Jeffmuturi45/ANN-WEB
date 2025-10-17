from django.contrib import admin
from django.http import HttpResponse
import csv
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from .models import Subscriber, ContactMessage

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed', 'active', 'source_page')
    search_fields = ('email',)
    list_filter = ('active',)
    actions = ['export_selected_emails_csv', 'export_selected_emails_txt', 'export_selected_full_data', 'send_newsletter_to_selected']
    
    # Add custom admin view for downloads and newsletter
    change_list_template = 'admin/newsletter/subscriber/change_list.html'
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('download-all-emails/', self.download_all_emails, name='download_all_emails'),
            path('download-all-subscribers/', self.download_all_subscribers, name='download_all_subscribers'),
            path('send-newsletter-to-all/', self.send_newsletter_to_all, name='send_newsletter_to_all'),
        ]
        return custom_urls + urls
    
    def download_all_emails(self, request):
        """Download all active subscriber emails as CSV"""
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f'all_active_emails_{timestamp}.csv'
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Date Subscribed', 'Source Page'])
        
        subscribers = Subscriber.objects.filter(active=True).order_by('date_subscribed')
        for subscriber in subscribers:
            writer.writerow([
                subscriber.email,
                subscriber.date_subscribed.strftime('%Y-%m-%d %H:%M:%S'),
                subscriber.source_page or 'N/A'
            ])
        
        self.message_user(request, f"✅ Exported {subscribers.count()} active emails to CSV")
        return response
    
    def download_all_subscribers(self, request):
        """Download all subscriber data as CSV"""
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f'all_subscribers_{timestamp}.csv'
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Date Subscribed', 'Status', 'Source Page'])
        
        subscribers = Subscriber.objects.all().order_by('-date_subscribed')
        for subscriber in subscribers:
            writer.writerow([
                subscriber.email,
                subscriber.date_subscribed.strftime('%Y-%m-%d %H:%M:%S'),
                'Active' if subscriber.active else 'Inactive',
                subscriber.source_page or 'N/A'
            ])
        
        self.message_user(request, f"✅ Exported {subscribers.count()} subscribers to CSV")
        return response
    
    def send_newsletter_to_all(self, request):
        """Send newsletter to all active subscribers"""
        if request.method == 'POST':
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            
            if not subject or not message:
                messages.error(request, "❌ Please provide both subject and message.")
                return self.changelist_view(request)
            
            subscribers = Subscriber.objects.filter(active=True)
            recipient_emails = [sub.email for sub in subscribers]
            
            if not recipient_emails:
                messages.error(request, "❌ No active subscribers to send to.")
                return self.changelist_view(request)
            
            try:
                # Send email to all subscribers
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.ADMIN_EMAIL],  # Send to yourself
                    bcc=recipient_emails,  # BCC to all subscribers
                )
                email.send()
                
                messages.success(request, f"✅ Newsletter sent successfully to {len(recipient_emails)} subscribers!")
                
            except Exception as e:
                messages.error(request, f"❌ Failed to send newsletter: {str(e)}")
        
        return self.changelist_view(request)
    
    def export_selected_emails_csv(self, request, queryset):
        """Action to export selected emails as CSV"""
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f'selected_emails_{timestamp}.csv'
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Date Subscribed', 'Status', 'Source Page'])
        
        for subscriber in queryset:
            writer.writerow([
                subscriber.email,
                subscriber.date_subscribed.strftime('%Y-%m-%d %H:%M:%S'),
                'Active' if subscriber.active else 'Inactive',
                subscriber.source_page or 'N/A'
            ])
        
        self.message_user(request, f"✅ Exported {queryset.count()} emails to CSV")
        return response
    
    export_selected_emails_csv.short_description = "📧 Export selected emails to CSV"
    
    def export_selected_emails_txt(self, request, queryset):
        """Action to export selected emails as plain text (one per line)"""
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f'selected_emails_{timestamp}.txt'
        
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        emails = [subscriber.email for subscriber in queryset]
        response.write('\n'.join(emails))
        
        self.message_user(request, f"✅ Exported {queryset.count()} emails to TXT")
        return response
    
    export_selected_emails_txt.short_description = "📄 Export selected emails to TXT"
    
    def export_selected_full_data(self, request, queryset):
        """Action to export full data for selected subscribers"""
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f'subscriber_data_{timestamp}.csv'
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Date Subscribed', 'Status', 'Source Page'])
        
        for subscriber in queryset:
            writer.writerow([
                subscriber.email,
                subscriber.date_subscribed.strftime('%Y-%m-%d %H:%M:%S'),
                'Active' if subscriber.active else 'Inactive',
                subscriber.source_page or 'N/A'
            ])
        
        self.message_user(request, f"✅ Exported full data for {queryset.count()} subscribers")
        return response
    
    export_selected_full_data.short_description = "📊 Export full data for selected subscribers"
    
    def send_newsletter_to_selected(self, request, queryset):
        """Action to send newsletter to selected subscribers"""
        recipient_emails = [sub.email for sub in queryset if sub.active]
        
        if not recipient_emails:
            messages.error(request, "❌ No active subscribers selected.")
            return
        
        # For simplicity, we'll use a default subject and message
        # You can enhance this later to show a form
        try:
            subject = "Newsletter Update"
            message = "Thank you for being a subscriber! Here's our latest update."
            
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
                bcc=recipient_emails,
            )
            email.send()
            
            messages.success(request, f"✅ Newsletter sent successfully to {len(recipient_emails)} selected subscribers!")
            
        except Exception as e:
            messages.error(request, f"❌ Failed to send newsletter: {str(e)}")
    
    send_newsletter_to_selected.short_description = "📧 Send newsletter to selected subscribers"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'created_at', 'read')
    search_fields = ('full_name', 'email', 'message')
    list_filter = ('read',)
    actions = ['mark_as_read', 'mark_as_unread', 'export_contact_messages']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(read=True)
        self.message_user(request, f"✅ Marked {updated} messages as read")
    
    mark_as_read.short_description = "📖 Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(read=False)
        self.message_user(request, f"✅ Marked {updated} messages as unread")
    
    mark_as_unread.short_description = "📭 Mark selected messages as unread"
    
    def export_contact_messages(self, request, queryset):
        """Export selected contact messages to CSV"""
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f'contact_messages_{timestamp}.csv'
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone', 'Message', 'Read', 'Date'])
        
        for message in queryset:
            writer.writerow([
                message.full_name,
                message.email,
                message.phone or 'N/A',
                message.message[:200] + '...' if len(message.message) > 200 else message.message,
                'Yes' if message.read else 'No',
                message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        self.message_user(request, f"✅ Exported {queryset.count()} contact messages to CSV")
        return response
    
    export_contact_messages.short_description = "📥 Export selected messages to CSV"