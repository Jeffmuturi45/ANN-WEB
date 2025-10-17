# newsletter/urls.py
from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('contact/', views.contact_view, name='contact'),
    path('unsubscribe/<uuid:token>/', views.unsubscribe_view, name='unsubscribe'),
    
     #path('send-newsletter/', views.send_newsletter, name='send_newsletter'),
]
