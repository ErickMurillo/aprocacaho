from django.shortcuts import render
from productores.models import *
from organizacion.models import *
from configuracion.models import *
from django.db.models import Sum, Count, Avg
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core import serializers
from django.contrib.auth.decorators import login_required

@login_required
def index(request,template="index.html"):
    socios = Encuesta.objects.filter(organizacionasociada__socio = '1').count()
    socios_mujeres = Encuesta.objects.filter(organizacionasociada__socio = '1',entrevistado__sexo = '1').count()
    socios_hombres = Encuesta.objects.filter(organizacionasociada__socio = '1',entrevistado__sexo = '2').count()

    organizaciones = Encuesta.objects.all().order_by('organizacion__nombre').distinct('organizacion__nombre').count()

    #areas cacao
    areas_cacao = Encuesta.objects.all().aggregate(total = Sum('plantacion__area'))['total']
    areas_mujeres = Encuesta.objects.filter(entrevistado__sexo = '1').aggregate(total = Sum('plantacion__area'))['total']
    areas_hombres = Encuesta.objects.filter(entrevistado__sexo = '2').aggregate(total = Sum('plantacion__area'))['total']

    #ProduccionCacao
    produccion = Encuesta.objects.all().aggregate(total = Sum('produccioncacao__cacao_baba'))['total'] / 100

    #total encuestas
    encuestas = Encuesta.objects.all().count()

    #miembros familia
    miembros = Encuesta.objects.all().aggregate(avg = Avg('familia__miembros'))['avg']

    #textos
    infogeneral = InfoGeneral.objects.all()[:1].get()
    sistema = SistemaInfo.objects.all()[:1].get()
    alcance = Alcance.objects.all()[:1].get()
    objetivo = Objetivo.objects.all()[:1].get()
    actualizacion = Actualizacion.objects.all()[:1].get()

    return render(request, template, locals())

class BusquedaView(TemplateView):
    def get(self, request, *args, **kwargs):
        id = request.GET['id']
        escuela_campo = EscuelaCampo.objects.filter(organizacion = id)
        data = serializers.serialize('json',escuela_campo,fields=('nombre',))
        return HttpResponse(data,content_type='application/json')
