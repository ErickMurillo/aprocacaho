from django.contrib import admin
from .models import *

# Register your models here.
#organizacion
class InlineEscuelaCampo(admin.TabularInline):
    model = EscuelaCampo
    extra = 1

class OrganizacionAdmin(admin.ModelAdmin):
    inlines = [InlineEscuelaCampo]
    list_display = ('id','nombre','siglas')
    list_display_links = ('id','nombre','siglas')

#encuesta organizacion
class InlineAspectosJuridicos(admin.TabularInline):
    model = AspectosJuridicos
    max_num = 1
    can_delete = False

class InlineListaMiembros(admin.TabularInline):
    model = ListaMiembros
    extra = 1

class InlineDocumentacion(admin.TabularInline):
    model = Documentacion
    extra = 1
    max_num = 7

class InlineProduccionComercializacion(admin.TabularInline):
    model = ProduccionComercializacion
    extra = 1

class InlineNivelCumplimiento(admin.TabularInline):
    model = NivelCumplimiento
    extra = 1
    max_num = 7

# class InlineDatosProductivos(admin.TabularInline):
#     model = DatosProductivos
#     extra = 1
#     max_num = 4
#
# class InlineDatosProductivosTabla(admin.TabularInline):
#     model = DatosProductivosTabla
#     extra = 1
#     max_num = 2

class InlineInfraestructura(admin.TabularInline):
    model = Infraestructura
    extra = 1

class InlineTransporte(admin.TabularInline):
    model = Transporte
    max_num = 1
    can_delete = False

# class InlineComercializacion(admin.TabularInline):
#     model = Comercializacion
#     extra = 1
#     max_num = 3
#
# class InlineCacaoComercializado(admin.TabularInline):
#     model = CacaoComercializado
#     max_num = 1
#     can_delete = False

class InlineCertificacionOrg(admin.TabularInline):
    model = CertificacionOrg
    max_num = 1
    can_delete = False

class InlineDestinoProdCorriente(admin.TabularInline):
    model = DestinoProdCorriente
    extra = 1
    max_num = 4

class InlineDestinoProdFermentado(admin.TabularInline):
    model = DestinoProdFermentado
    extra = 1
    max_num = 4

class InlineFinanciamiento(admin.TabularInline):
    model = Financiamiento
    max_num = 1
    can_delete = False

class InlineFinanciamientoProductores(admin.TabularInline):
    model = FinanciamientoProductores
    extra = 1
    max_num = 5

class InlineInfoFinanciamiento(admin.TabularInline):
    model = InfoFinanciamiento
    extra = 1
    max_num = 4

class EncuestaOrganicacionAdmin(admin.ModelAdmin):
    # def get_queryset(self, request):
    #     if request.user.is_superuser:
    #         return EncuestaOrganicacion.objects.all()
    #     return EncuestaOrganicacion.objects.filter(usuario=request.user)

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()

    inlines = [InlineAspectosJuridicos,InlineListaMiembros,InlineDocumentacion,
                InlineNivelCumplimiento,InlineProduccionComercializacion,
                InlineInfraestructura,InlineTransporte,
                InlineCertificacionOrg,InlineDestinoProdCorriente,InlineDestinoProdFermentado,
                InlineFinanciamiento,InlineFinanciamientoProductores,InlineInfoFinanciamiento]

    list_display = ('id','organizacion','fecha')
    list_display_links = ('id','organizacion')

    class Media:
        css = {
            'all': ('css/admin.css',)
        }
        js = ('js/admin_org.js',)


admin.site.register(Organizacion,OrganizacionAdmin)
admin.site.register(EncuestaOrganicacion,EncuestaOrganicacionAdmin)
