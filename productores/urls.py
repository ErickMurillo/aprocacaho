from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    url(r'^$', consulta_productores, name='consulta-productores'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^educacion/$', educacion, name='educacion'),
    url(r'^tenencia-propiedad/$', tenencia_propiedad, name='tenencia-propiedad'),
    url(r'^uso-tierra/$', uso_tierra, name='uso-tierra'),
    url(r'^reforestacion/$', reforestacion, name='reforestacion'),
    url(r'^caracterizacion-terreno/$', caracterizacion_terreno, name='caracterizacion-terreno'),
    url(r'^riesgos-finca/$', riesgos_finca, name='riesgos-finca'),
    url(r'^mitigacion-riesgos/$', mitigacion_riesgos, name='mitigacion-riesgos'),
    url(r'^organizacion-productiva/$', organizacion_productiva, name='organizacion-productiva'),
    url(r'^produccion/$', produccion, name='produccion'),

    url(r'^ajax/munis/$', get_munis, name='get-munis'),
    url(r'^ajax/comunies/$', get_comunies, name='get-comunies'),
    url(r'^ajax/organi/$', get_organi, name='get-organi'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
