from django.contrib import admin
from .models import *

# Register your models here.
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

class InlineNivelCumplimiento(admin.TabularInline):
    model = NivelCumplimiento
    extra = 1
    max_num = 7

class InlineDatosProductivos(admin.TabularInline):
    model = DatosProductivos
    max_num = 1
    can_delete = False

class InlineDatosProductivosTabla(admin.TabularInline):
    model = DatosProductivosTabla
    extra = 1
    max_num = 5

class InlineInfraestructura(admin.TabularInline):
    model = Infraestructura
    extra = 1
    max_num = 11

class InlineComercializacion(admin.TabularInline):
    model = Comercializacion
    extra = 1
    max_num = 4

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
    extra = 1
    max_num = 4

class InlineFinanciamientoProductores(admin.TabularInline):
    model = FinanciamientoProductores
    max_num = 1
    can_delete = False

class InlineRespuestaSi(admin.TabularInline):
    model = RespuestaSi
    max_num = 1
    can_delete = False

class EncuestaOrganicacionAdmin(admin.ModelAdmin):
    # def get_queryset(self, request):
    #     if request.user.is_superuser:
    #         return EncuestaOrganicacion.objects.all()
    #     return EncuestaOrganicacion.objects.filter(usuario=request.user)

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()

    inlines = [InlineAspectosJuridicos,InlineListaMiembros,InlineDocumentacion,
                InlineNivelCumplimiento,InlineDatosProductivos,InlineDatosProductivosTabla,
                InlineInfraestructura,InlineComercializacion,InlineCertificacionOrg,
                InlineDestinoProdCorriente,InlineDestinoProdFermentado,InlineFinanciamiento,
                InlineFinanciamientoProductores,InlineRespuestaSi]

    class Media:
        css = {
            'all': ('css/admin.css',)
        }
        js = ('js/admin_org.js',)


admin.site.register(Organizacion)
admin.site.register(EncuestaOrganicacion,EncuestaOrganicacionAdmin)
