# newsletter/forms.py
from django import forms

class SubscribeForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'you@domain.com'}))

class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=50, required=False)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    
    
# NewsletterForm

class NewsletterForm(forms.Form):
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter newsletter subject',
            'required': True
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your newsletter content...',
            'rows': 12,
            'required': True
        })
    )
