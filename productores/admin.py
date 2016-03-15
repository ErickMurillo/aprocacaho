# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

# Register your models here.

class EncuestaAdmin(admin.ModelAdmin):
	def get_queryset(self, request):
		if request.user.is_superuser:
			return Encuesta.objects.all()
		return Encuesta.objects.filter(usuario=request.user)

	def save_model(self, request, obj, form, change):
		if request.user.is_superuser:
			obj.save()
		else:
			obj.usuario = request.user
			obj.save()

	def get_form(self, request, obj=None, **kwargs):
		if request.user.is_superuser:
			self.exclude = ('anno',)
			self.fieldsets = [(('Información del Entrevistado'), {'fields' : (('fecha',),('organizacion','encuestador'),('entrevistado','usuario'))}),]
		else:
			self.exclude = ('usuario','anno')
			self.fieldsets = [(('Información del Entrevistado'), {'fields' : (('fecha',),('organizacion','encuestador'),('entrevistado',))}),]
		return super(EncuestaAdmin, self).get_form(request, obj=None, **kwargs)

	def get_list_filter(self, request):
		if request.user.is_superuser:
			return ('organizacion',)
		else:
			return ()

	list_display = ('entrevistado','organizacion','encuestador')
	list_display_links = ('organizacion','entrevistado')
	search_fields = ['entrevistado__nombre','encuestador__nombre']


admin.site.register(Profesiones)
admin.site.register(Entrevistados)
admin.site.register(Encuestadores)
admin.site.register(Encuesta,EncuestaAdmin)
