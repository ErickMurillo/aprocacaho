from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    url(r'^$', consulta_org, name='consulta-org'),
    url(r'^detalle/(?P<slug>[\w-]+)/$', detail_org, name='detail-org'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
