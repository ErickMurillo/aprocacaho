# -*- coding: utf-8 -*-
"""aprocacaho URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from utils import *
from django.contrib.auth import views as auth_views

admin.site.site_header = "Administración APROCACAHO"
admin.site.site_title = "Administración APROCACAHO"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^$', index, name='index'),
    url(r'^productores/', include('productores.urls')),
    url(r'^organizaciones/', include('organizacion.urls')),
    url(r'^xls/$', save_as_xls),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}),
    url(r'^logout/$', auth_views.logout,{'next_page': '/'}),
    url(r'^admin/escuela-campo/$', BusquedaView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
