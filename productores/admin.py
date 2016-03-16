# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

# Register your models here.
class Familia_Inline(admin.TabularInline):
	model = Familia
	max_num = 1
	can_delete = False

class Educacion_Inline(admin.TabularInline):
	model = Educacion
	extra = 1
	max_num = 10

class TenenciaPropiedad_Inline(admin.TabularInline):
	model = TenenciaPropiedad
	max_num = 1
	can_delete = False

class AreaFinca_Inline(admin.TabularInline):
	model = AreaFinca
	max_num = 1
	can_delete = False

class DetalleAreaFinca_Inline(admin.TabularInline):
	model = DetalleAreaFinca
	max_num = 11
	extra = 1

class Reforestacion_Inline(admin.TabularInline):
	model = Reforestacion
	max_num = 8
	extra = 1

class CaracterizacionTerreno_Inline(admin.TabularInline):
	model = CaracterizacionTerreno
	max_num = 1
	can_delete = False

class FenomenosNaturales_Inline(admin.TabularInline):
	model = FenomenosNaturales
	max_num = 1
	can_delete = False

class RazonesAgricolas_Inline(admin.TabularInline):
	model = RazonesAgricolas
	max_num = 1
	can_delete = False

class RazonesMercado_Inline(admin.TabularInline):
	model = RazonesMercado
	max_num = 1
	can_delete = False

class Inversion_Inline(admin.TabularInline):
	model = Inversion
	max_num = 1
	can_delete = False

class MitigacionRiesgos_Inline(admin.TabularInline):
	model = MitigacionRiesgos
	max_num = 1
	can_delete = False

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

	inlines = [Familia_Inline,Educacion_Inline,TenenciaPropiedad_Inline,AreaFinca_Inline,DetalleAreaFinca_Inline,
				Reforestacion_Inline,CaracterizacionTerreno_Inline,FenomenosNaturales_Inline,RazonesAgricolas_Inline,
				RazonesMercado_Inline,Inversion_Inline,MitigacionRiesgos_Inline]

	list_display = ('entrevistado','organizacion','encuestador')
	list_display_links = ('organizacion','entrevistado')
	search_fields = ['entrevistado__nombre','encuestador__nombre']


admin.site.register(Profesiones)
admin.site.register(SituacionesPropiedad)
admin.site.register(Entrevistados)
admin.site.register(Encuestadores)
admin.site.register(Encuesta,EncuestaAdmin)
