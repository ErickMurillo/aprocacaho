from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    url(r'^$', consulta_productores, name='consulta-productores'),
    url(r'^dashboard/$', dashboard, name='dashboard'),

    url(r'^ajax/munis/$', get_munis, name='get-munis'),
    url(r'^ajax/comunies/$', get_comunies, name='get-comunies'),
    url(r'^ajax/organi/$', get_organi, name='get-organi'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
