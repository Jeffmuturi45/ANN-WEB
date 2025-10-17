"""
URL configuration for annweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from newsletter import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('newsletter.urls', namespace='newsletter')),
     path('', views.home, name='home'), 
     path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
     path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
     path('ignite/', TemplateView.as_view(template_name='ignite.html'), name='ignite'),
     path('journal/', TemplateView.as_view(template_name='journal.html'), name='journal'),
     path('journal1/', TemplateView.as_view(template_name='journal1.html'), name='journal1'),
     path('journal2/', TemplateView.as_view(template_name='journal2.html'), name='journal2'),
     path('journal3/', TemplateView.as_view(template_name='journal3.html'), name='journal3'),
     path('journal4/', TemplateView.as_view(template_name='journal4.html'), name='journal4'),
     path('journal5/', TemplateView.as_view(template_name='journal5.html'), name='journal5'),
     path('journal6/', TemplateView.as_view(template_name='journal6.html'), name='journal6'),
     path('journal7/', TemplateView.as_view(template_name='journal7.html'), name='journal7'),
     path('journal8/', TemplateView.as_view(template_name='journal8.html'), name='journal8'),
     path('journal9/', TemplateView.as_view(template_name='journal9.html'), name='journal9'),
     path('journal10/', TemplateView.as_view(template_name='journal10.html'), name='journal10'),
     path('leadership_coaching/', TemplateView.as_view(template_name='leadership_coaching.html'), name='leadership_coaching'),
    path('leadership_consultancy/', TemplateView.as_view(template_name='leadership_consultancy.html'), name='leadership_consultancy'),
    path('leadership_workshops/', TemplateView.as_view(template_name='leadership_workshops.html'), name='leadership_workshops'),
    path('podcast/', TemplateView.as_view(template_name='podcast.html'), name='podcast'),
    path('shop/', TemplateView.as_view(template_name='shop.html'), name='shop'),
    path('speaking/', TemplateView.as_view(template_name='speaking.html'), name='speaking'),
    path('values/', TemplateView.as_view(template_name='values.html'), name='values'),
    path('vision/', TemplateView.as_view(template_name='vision.html'), name='vision'),
    path('send_newsletter/', TemplateView.as_view(template_name='send_newsletter.html'), name='send_newsletter'),    
]
