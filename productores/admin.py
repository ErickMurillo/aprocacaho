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

class OrganizacionAsociada_Inline(admin.TabularInline):
	model = OrganizacionAsociada
	max_num = 1
	can_delete = False

class ServiciosOrganizado_Inline(admin.TabularInline):
	model = ServiciosOrganizado
	max_num = 1
	can_delete = False

class BeneficiosOrganizado_Inline(admin.TabularInline):
	model = BeneficiosOrganizado
	max_num = 1
	can_delete = False

class AreaCacao_Inline(admin.TabularInline):
	model = AreaCacao
	max_num = 1
	can_delete = False

class Plantacion_Inline(admin.TabularInline):
	model = Plantacion
	max_num = 5
	extra = 1

class ProduccionCacao_Inline(admin.TabularInline):
	model = ProduccionCacao
	max_num = 1
	can_delete = False

class DistribucionProduccionCacao_Inline(admin.TabularInline):
	model = DistribucionProduccionCacao
	extra = 1

class Certificacion_Inline(admin.TabularInline):
	model = Certificacion
	max_num = 1
	can_delete = False

class CostoProduccion_Inline(admin.TabularInline):
	model = CostoProduccion
	max_num = 1
	can_delete = False

class TecnicasAplicadas_Inline(admin.StackedInline):
	model = TecnicasAplicadas
	max_num = 1
	can_delete = False

class ComercializacionCacao_Inline(admin.TabularInline):
	model = ComercializacionCacao
	extra = 1

class DistanciaComercioCacao_Inline(admin.TabularInline):
	model = DistanciaComercioCacao
	max_num = 1
	can_delete = False

class CapacitacionesTecnicas_Inline(admin.TabularInline):
	model = CapacitacionesTecnicas
	max_num = 11
	extra = 1

class CapacitacionesSocioeconomicas_Inline(admin.TabularInline):
	model = CapacitacionesSocioeconomicas
	max_num = 8
	extra = 1

class ProblemasAreaCacao_Inline(admin.TabularInline):
	model = ProblemasAreaCacao
	max_num = 1
	can_delete = False

class Genero_Inline(admin.StackedInline):
	model = Genero
	max_num = 1
	can_delete = False
	fieldsets = [(None,
				{'fields' : (('actividades'),('ingresos','ingreso_mesual_cacao','ingreso_mesual'),('destino_ingresos',),('decisiones',),('otros_ingresos',))}),
	]

class AmpliarAreasCacao_Inline(admin.TabularInline):
	model = AmpliarAreasCacao
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
				RazonesMercado_Inline,Inversion_Inline,MitigacionRiesgos_Inline,OrganizacionAsociada_Inline,
				ServiciosOrganizado_Inline,BeneficiosOrganizado_Inline,AreaCacao_Inline,Plantacion_Inline,
				ProduccionCacao_Inline,DistribucionProduccionCacao_Inline,Certificacion_Inline,CostoProduccion_Inline,TecnicasAplicadas_Inline,
				ComercializacionCacao_Inline,DistanciaComercioCacao_Inline,CapacitacionesTecnicas_Inline,
				CapacitacionesSocioeconomicas_Inline,ProblemasAreaCacao_Inline,Genero_Inline,AmpliarAreasCacao_Inline]

	list_display = ('id','entrevistado','organizacion','encuestador','fecha')
	list_display_links = ('organizacion','entrevistado')
	search_fields = ['entrevistado__nombre','encuestador__nombre']

	class Media:
		js = ('js/admin.js',)
		css = {
			'all': ('css/admin.css',)
		}

class EntrevistadosAdmin(admin.ModelAdmin):
	list_display = ('id','nombre','organizacion')
	list_display_links = ('id','nombre')
	search_fields = ['nombre','cedula','organizacion']

	class Media:
		js = ('js/entrevistados.js',)

class EncuestadoresAdmin(admin.ModelAdmin):
	list_display = ('id','nombre','organizacion')
	list_display_links = ('id','nombre')
	search_fields = ['nombre','organizacion']

admin.site.register(Profesiones)
admin.site.register(SituacionesPropiedad)
admin.site.register(Beneficios)
admin.site.register(QuienCertifica)
admin.site.register(TiposServicio)
admin.site.register(ActividadesProduccion)
admin.site.register(DestinoIngresos)
admin.site.register(OtrosIngresos)
admin.site.register(ProblemasArea1)
admin.site.register(ProblemasArea2)
admin.site.register(ProblemasArea3)
admin.site.register(Entrevistados,EntrevistadosAdmin)
admin.site.register(Encuestadores,EncuestadoresAdmin)
admin.site.register(Encuesta,EncuestaAdmin)
