# newsletter/views.py
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # don't use unless necessary
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from .models import Subscriber, ContactMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import NewsletterForm
from django.template import TemplateDoesNotExist



logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'speaking.html')

def contact_page(request):  # Different name from contact form view
    return render(request, 'contact.html')

def ignite(request):
    return render(request, 'ignite.html')

def journal(request):
    return render(request, 'journal.html')

def journal1(request):
    return render(request, 'journal1.html')

def journal2(request):
    return render(request, 'journal2.html')

def journal3(request):
    return render(request, 'journal3.html')

def journal4(request):
    return render(request, 'journal4.html')

def journal5(request):
    return render(request, 'journal5.html')

def journal6(request):
    return render(request, 'journal6.html')

def journal7(request):
    return render(request, 'journal7.html')

def journal8(request):
    return render(request, 'journal8.html')

def journal9(request):
    return render(request, 'journal9.html')

def journal10(request):
    return render(request, 'journal10.html')

def leadership_coaching(request):
    return render(request, 'leadership_coaching.html')

def leadership_consultancy(request):
    return render(request, 'leadership_consultancy.html')

def leadership_workshops(request):
    return render(request, 'leadership_workshops.html')

def podcast(request):
    return render(request, 'podcast.html')

def shop(request):
    return render(request, 'shop.html')

def speaking(request):
    return render(request, 'speaking.html')

def values(request):
    return render(request, 'values.html')

def vision(request):
    return render(request, 'vision.html')


@require_POST
def subscribe_view(request):
    """
    POST handler for subscription. Accepts form-encoded data or Ajax.
    Expects 'email' and optional 'source'.
    Returns JSON { success: bool, message/error: str }.
    """
    email = request.POST.get('email') or request.GET.get('email')
    source = request.POST.get('source', request.META.get('HTTP_REFERER', ''))

    if not email:
        return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)

    # Validate email format
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'success': False, 'error': 'Invalid email address'}, status=400)

    # Save subscriber
    try:
        with transaction.atomic():
            subscriber, created = Subscriber.objects.get_or_create(
                email=email.lower(), 
                defaults={'source_page': source}
            )
            if not created:
                if not subscriber.active:
                    subscriber.active = True
                    subscriber.save()
                return JsonResponse({'success': True, 'message': 'This email is already subscribed.'})
    except IntegrityError:
        logger.exception("Database error while creating subscriber")
        return JsonResponse({'success': False, 'error': 'Database error'}, status=500)
    except Exception:
        logger.exception("Unexpected error while creating subscriber")
        return JsonResponse({'success': False, 'error': 'Server error'}, status=500)

    # Send enhanced welcome email to new subscriber
    try:
        context = {
            'subscriber': subscriber,
            'unsubscribe_link': f"{request.scheme}://{request.get_host()}/unsubscribe/{getattr(subscriber, 'unsubscribe_token', 'default')}/",
            'site_url': f"{request.scheme}://{request.get_host()}"
        }
        
        subject = "🎉 Welcome to Annastacia's Newsletter!"
        
        # Force use of templates by checking if they exist
        try:
            # Try to render the HTML template
            html_body = render_to_string('emails/welcome.html', context)
        except TemplateDoesNotExist:
            # Fallback HTML if template doesn't exist
            html_body = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: #667eea; color: white; padding: 30px; text-align: center; }
                    .content { padding: 30px; background: #f9f9f9; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Welcome to Our Community! 🎉</h1>
                    </div>
                    <div class="content">
                        <h2>Hello there!</h2>
                        <p>Thank you for subscribing to Annastacia's newsletter. We're thrilled to have you join our community!</p>
                        
                        <p><strong>Here's what you can look forward to:</strong></p>
                        <ul>
                            <li>✨ Exclusive content and early access</li>
                            <li>🎨 Creative inspiration and insights</li>
                            <li>📰 Latest updates and news</li>
                            <li>💡 Professional tips and guidance</li>
                            <li>🎁 Special offers just for subscribers</li>
                        </ul>
                        
                        <p>We're committed to bringing you valuable content that inspires and informs.</p>
                        
                        <p>Stay amazing!<br>
                        <strong>The Annastacia Team</strong></p>
                    </div>
                </div>
            </body>
            </html>
            """
        
        try:
            # Try to render the text template
            text_body = render_to_string('emails/welcome.txt', context)
        except TemplateDoesNotExist:
            # Fallback text if template doesn't exist
            text_body = f"""
Welcome to Our Community! 🎉

Hello there!

Thank you for subscribing to Annastacia's newsletter. We're thrilled to have you join our community!

Here's what you can look forward to:

✨ Exclusive content and early access
🎨 Creative inspiration and insights  
📰 Latest updates and news
💡 Professional tips and guidance
🎁 Special offers just for subscribers

We're committed to bringing you valuable content that inspires and informs.

Stay amazing!
The Annastacia Team

Visit us: {context['site_url']}
            """
        
        msg = EmailMultiAlternatives(
            subject, 
            text_body, 
            settings.DEFAULT_FROM_EMAIL, 
            [subscriber.email]
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        
        logger.info(f"✅ Welcome email sent successfully to {subscriber.email}")
        
    except Exception as e:
        logger.error(f"❌ Failed to send welcome email to {subscriber.email}: {str(e)}")
        # Don't fail the subscription if email fails

    # Notify Annastacia of new subscription
    try:
        annastacia_email = "annastacia@annastaciawainaina.com"
        total_subscribers = Subscriber.objects.filter(active=True).count()
        
        subject = "🎉 New Newsletter Subscriber!"
        
        body = f"""
Great news Annastacia!

You have a new newsletter subscriber:

📧 Email: {subscriber.email}
📍 Source: {source or 'Direct'}
📅 Date: {subscriber.date_subscribed.strftime('%Y-%m-%d %H:%M')}
        
📊 Current Statistics:
Total Active Subscribers: {total_subscribers}

Keep up the amazing work! Your content is building a wonderful community.

---
Automated notification from your website
        """
        
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [annastacia_email])
        logger.info(f"✅ Subscription notification sent to Annastacia for: {subscriber.email}")
        
    except Exception as e:
        logger.error(f"❌ Failed to notify Annastacia: {str(e)}")

    return JsonResponse({'success': True, 'message': 'Subscribed successfully! Welcome email sent.'})



def contact_view(request):
    # Serve the frontend page if accessed via GET
    if request.method == "GET":
        return render(request, "contact.html")

    # Extract POST data
    full_name = request.POST.get('full_name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip().lower()
    message_text = request.POST.get('message', '').strip()

    # Validate
    if not full_name:
        return JsonResponse({'success': False, 'error': 'Full name is required.'}, status=400)
    if not email:
        return JsonResponse({'success': False, 'error': 'Email is required.'}, status=400)
    if not message_text:
        return JsonResponse({'success': False, 'error': 'Message is required.'}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'success': False, 'error': 'Invalid email address.'}, status=400)

    # Save message to database
    contact = ContactMessage.objects.create(
        full_name=full_name, phone=phone, email=email, message=message_text
    )

    # Fetch admin recipient safely
    admin_email = "annastacia@annastaciawainaina.com"


    # Prepare email
    subject = f"📨 New Contact Form Message from {full_name}"
    body = f"""
You received a new message from your website:

👤 Name: {full_name}
📧 Email: {email}
📞 Phone: {phone or 'Not provided'}

📝 Message:
{message_text}

---
This message was auto-generated by your website.
    """.strip()

    # Send to admin
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [admin_email])
        print("✅ Admin email sent successfully!")
    except Exception as e:
        print("❌ Failed to send admin email:", e)

    # Auto confirmation to user
    try:
        context = {'contact': contact, 'full_name': full_name}
        confirmation_subject = "✅ We've received your message!"
        text_body = render_to_string('emails/contact_thanks.txt', context)

        msg = EmailMultiAlternatives(confirmation_subject, text_body, settings.DEFAULT_FROM_EMAIL, [email])

        try:
            html_body = render_to_string('emails/contact_thanks.html', context)
            msg.attach_alternative(html_body, "text/html")
        except:
            pass

        msg.send()
        print("✅ Confirmation email sent to user.")
    except Exception as e:
        print("⚠️ Failed to send confirmation email:", e)

    return JsonResponse({'success': True, 'message': 'Message sent successfully. Thank you for contacting us!'})


def unsubscribe_view(request, token):
    """
    GET link that deactivates the subscription tied to token.
    """
    try:
        sub = get_object_or_404(Subscriber, unsubscribe_token=token)
        sub.active = False
        sub.save()
        return HttpResponse("You have been unsubscribed. Thank you.")
    except Exception:
        logger.exception("Error during unsubscribe")
        return HttpResponse("Unable to unsubscribe at this time.", status=500)
    
    
