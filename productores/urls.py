from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    url(r'^$', consulta_productores, name='consulta-productores'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
