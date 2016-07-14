from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    url(r'^$', consulta_org, name='consulta-org'),
    url(r'^detalle/(?P<slug>[\w-]+)/$', detail_org, name='detail-org'),
    url(r'^estatus-legal/$', estatus_legal, name='estatus-legal'),
    url(r'^aspectos-juridicos/$', aspectos_juridicos, name='aspectos-juridicos'),
    url(r'^documentacion/$', documentacion, name='documentacion'),
    url(r'^datos-productivos/$', datos_productivos, name='datos-productivos'),
    url(r'^instalaciones-y-equipos/$', instalaciones, name='instalaciones-y-equipos'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
