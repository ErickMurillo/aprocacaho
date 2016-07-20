from django.shortcuts import render
from productores.models import *
from organizacion.models import *
from django.db.models import Sum, Count, Avg

def index(request,template="index.html"):
    socios = Encuesta.objects.filter(organizacionasociada__socio = '1').count()
    socios_mujeres = Encuesta.objects.filter(organizacionasociada__socio = '1',entrevistado__sexo = '1').count()
    socios_hombres = Encuesta.objects.filter(organizacionasociada__socio = '1',entrevistado__sexo = '2').count()

    organizaciones = Encuesta.objects.all().order_by('organizacion__nombre').distinct().count()

    #areas cacao
    areas_cacao = Encuesta.objects.all().aggregate(total = Sum('plantacion__area'))['total']
    areas_mujeres = Encuesta.objects.filter(entrevistado__sexo = '1').aggregate(total = Sum('plantacion__area'))['total']
    areas_hombres = Encuesta.objects.filter(entrevistado__sexo = '2').aggregate(total = Sum('plantacion__area'))['total']

    #ProduccionCacao
    produccion = Encuesta.objects.all().aggregate(total = Sum('produccioncacao__cacao_baba'))['total']

    return render(request, template, locals())
